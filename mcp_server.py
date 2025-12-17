#!/usr/bin/env python3
"""
CipherBot MCP Server - Fixed version for proper JSON-RPC communication
Ethical hacking tools for authorized security testing
"""
import os
import sys
import subprocess
import re
from pathlib import Path

# CRITICAL FIX: Disable all logging to prevent JSON corruption
import logging
logging.basicConfig(level=logging.CRITICAL, handlers=[])

from mcp.server.fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("cipherbot")

# Safe tools whitelist
SAFE_TOOLS = {
    "nmap", "amass", "subfinder", "assetfinder", "httpx",
    "aquatone", "theharvester", "ffuf", "gobuster", "dirsearch",
    "wfuzz", "sqlmap", "xsstrike", "nuclei", "nikto", "whatweb",
    "masscan", "rustscan", "feroxbuster", "katana", "sublist3r",
    "dnsenum", "fierce", "wafw00f", "commix", "joomscan"
}

# Tools that need sudo
SUDO_TOOLS = {"nmap", "nikto", "sqlmap", "nuclei", "masscan", "rustscan"}

# Filesystem base path (mounted from host)
HOST_FS_BASE = "/host"

def sanitize_input(text: str) -> str:
    """Sanitize input to prevent command injection."""
    text = text.strip()
    text = re.sub(r'[;&|`$<>]', '', text)
    return text

def sanitize_path(path: str) -> str:
    """Sanitize filesystem paths to prevent directory traversal."""
    path = os.path.normpath(path)
    return path.lstrip('/')

def sanitize_package_name(package: str) -> str:
    """Sanitize package names for apt operations."""
    package = re.sub(r'[^a-zA-Z0-9\-_\.]', '', package.strip())
    return package

def run_command(cmd, timeout=600, use_sudo=False):
    """Execute command safely and return results."""
    try:
        if use_sudo:
            cmd = ["sudo"] + cmd
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)

# ========== PACKAGE MANAGEMENT TOOLS ==========

@mcp.tool()
async def install_tool(package: str = "") -> str:
    """
    Install a new security tool or package using apt (requires explicit user permission).
    This uses sudo to install packages system-wide.
    """
    if not package.strip():
        return "Error: Package name is required"
    
    package = sanitize_package_name(package)
    if not package:
        return "Error: Invalid package name"
    
    # Update apt cache first
    returncode, stdout, stderr = run_command(["apt", "update"], timeout=300)
    
    if returncode != 0:
        return f"Error updating apt cache:\n{stderr}"
    
    # Install the package
    cmd = ["apt", "install", "-y", package]
    returncode, stdout, stderr = run_command(cmd, timeout=600)
    
    if returncode == 0:
        SAFE_TOOLS.add(package)
        return f"Successfully installed: {package}\n\nOutput:\n{stdout}\n\nPackage has been added to available tools."
    else:
        return f"Failed to install {package}:\n{stderr}\n\nOutput:\n{stdout}"

@mcp.tool()
async def search_tool(query: str = "") -> str:
    """
    Search for available packages in apt repositories.
    Useful for finding security tools before installing them.
    """
    if not query.strip():
        return "Error: Search query is required"
    
    query = sanitize_package_name(query)
    if not query:
        return "Error: Invalid search query"
    
    cmd = ["apt", "search", query]
    returncode, stdout, stderr = run_command(cmd, timeout=120)
    
    if returncode == 0 or stdout:
        return f"Search results for '{query}':\n\n{stdout}"
    else:
        return f"Search failed:\n{stderr}"

@mcp.tool()
async def remove_tool(package: str = "") -> str:
    """
    Remove an installed package using apt (requires explicit user permission).
    This uses sudo to remove packages system-wide.
    """
    if not package.strip():
        return "Error: Package name is required"
    
    package = sanitize_package_name(package)
    if not package:
        return "Error: Invalid package name"
    
    cmd = ["apt", "remove", "-y", package]
    returncode, stdout, stderr = run_command(cmd, timeout=300)
    
    if returncode == 0:
        SAFE_TOOLS.discard(package)
        return f"Successfully removed: {package}\n\nOutput:\n{stdout}"
    else:
        return f"Failed to remove {package}:\n{stderr}\n\nOutput:\n{stdout}"

@mcp.tool()
async def list_installed_tools() -> str:
    """
    List all currently installed security tools and packages.
    """
    cmd = ["dpkg", "-l"]
    returncode, stdout, stderr = run_command(cmd, timeout=60)
    
    if returncode == 0:
        return f"Installed packages:\n\n{stdout}"
    else:
        return f"Failed to list packages:\n{stderr}"

@mcp.tool()
async def install_pip_package(package: str = "") -> str:
    """
    Install a Python package using pip in the virtual environment.
    Useful for Python-based security tools.
    """
    if not package.strip():
        return "Error: Package name is required"
    
    package = sanitize_package_name(package)
    if not package:
        return "Error: Invalid package name"
    
    cmd = ["/opt/cipherbot-venv/bin/pip", "install", package]
    returncode, stdout, stderr = run_command(cmd, timeout=600)
    
    if returncode == 0:
        return f"Successfully installed Python package: {package}\n\nOutput:\n{stdout}"
    else:
        return f"Failed to install {package}:\n{stderr}\n\nOutput:\n{stdout}"

# ========== FILESYSTEM TOOLS ==========

@mcp.tool()
async def fs_read(path: str = "") -> str:
    """
    Read file from host filesystem (requires explicit user permission).
    Path is relative to mounted /host directory.
    """
    if not path.strip():
        return "Error: Path is required"
    
    safe_path = sanitize_path(path)
    full_path = os.path.join(HOST_FS_BASE, safe_path)
    
    try:
        if not os.path.exists(full_path):
            return f"Error: File not found: {path}"
        
        if not os.path.isfile(full_path):
            return f"Error: Not a file: {path}"
        
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return f"File: {path}\n\nContent:\n{content}"
    
    except PermissionError:
        return f"Error: Permission denied: {path}"
    except UnicodeDecodeError:
        return f"Error: File appears to be binary. Cannot read as text: {path}"
    except Exception as e:
        return f"Error reading file: {str(e)}"

@mcp.tool()
async def fs_write(path: str = "", content: str = "") -> str:
    """
    Write content to file on host filesystem (requires explicit user permission).
    Path is relative to mounted /host directory.
    """
    if not path.strip():
        return "Error: Path is required"
    
    if not content:
        return "Error: Content cannot be empty"
    
    safe_path = sanitize_path(path)
    full_path = os.path.join(HOST_FS_BASE, safe_path)
    
    try:
        # Create parent directories if needed
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return f"Success: Written {len(content)} bytes to {path}"
    
    except PermissionError:
        return f"Error: Permission denied: {path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

@mcp.tool()
async def fs_execute(path: str = "", arguments: str = "") -> str:
    """
    Execute a script/binary from host filesystem (requires explicit user permission).
    Path is relative to mounted /host directory.
    """
    if not path.strip():
        return "Error: Path is required"
    
    safe_path = sanitize_path(path)
    full_path = os.path.join(HOST_FS_BASE, safe_path)
    
    try:
        if not os.path.exists(full_path):
            return f"Error: File not found: {path}"
        
        if not os.access(full_path, os.X_OK):
            return f"Error: File is not executable: {path}"
        
        # Parse arguments
        args_list = []
        if arguments.strip():
            args_list = arguments.strip().split()
            args_list = [sanitize_input(arg) for arg in args_list]
        
        cmd = [full_path] + args_list
        returncode, stdout, stderr = run_command(cmd, timeout=300)
        
        if returncode == 0:
            return f"Executed: {path}\n\nOutput:\n{stdout}"
        else:
            return f"Executed: {path}\nExit code: {returncode}\n\nStderr:\n{stderr}\n\nStdout:\n{stdout}"
    
    except PermissionError:
        return f"Error: Permission denied: {path}"
    except Exception as e:
        return f"Error executing file: {str(e)}"

@mcp.tool()
async def fs_list(path: str = ".") -> str:
    """
    List directory contents on host filesystem.
    Path is relative to mounted /host directory.
    """
    safe_path = sanitize_path(path)
    full_path = os.path.join(HOST_FS_BASE, safe_path)
    
    try:
        if not os.path.exists(full_path):
            return f"Error: Directory not found: {path}"
        
        if not os.path.isdir(full_path):
            return f"Error: Not a directory: {path}"
        
        items = []
        for item in sorted(os.listdir(full_path)):
            item_path = os.path.join(full_path, item)
            try:
                if os.path.isdir(item_path):
                    items.append(f"[DIR]  {item}")
                else:
                    stat_info = os.lstat(item_path)
                    size = stat_info.st_size
                    if os.path.islink(item_path):
                        items.append(f"[LINK] {item} ({size} bytes)")
                    else:
                        items.append(f"[FILE] {item} ({size} bytes)")
            except (OSError, PermissionError) as e:
                items.append(f"[????] {item} (error: {str(e)})")
        
        return f"Directory listing: {path}\n\n" + "\n".join(items)
    
    except PermissionError:
        return f"Error: Permission denied: {path}"
    except Exception as e:
        return f"Error listing directory: {str(e)}"

@mcp.tool()
async def fs_mkdir(path: str = "") -> str:
    """
    Create a directory on host filesystem (requires explicit user permission).
    Path is relative to mounted /host directory.
    """
    if not path.strip():
        return "Error: Path is required"
    
    safe_path = sanitize_path(path)
    full_path = os.path.join(HOST_FS_BASE, safe_path)
    
    try:
        os.makedirs(full_path, exist_ok=True)
        return f"Success: Created directory {path}"
    
    except PermissionError:
        return f"Error: Permission denied: {path}"
    except Exception as e:
        return f"Error creating directory: {str(e)}"

@mcp.tool()
async def fs_delete(path: str = "") -> str:
    """
    Delete a file or directory from host filesystem (requires explicit user permission).
    Path is relative to mounted /host directory.
    WARNING: This permanently deletes files!
    """
    if not path.strip():
        return "Error: Path is required"
    
    safe_path = sanitize_path(path)
    full_path = os.path.join(HOST_FS_BASE, safe_path)
    
    try:
        if not os.path.exists(full_path):
            return f"Error: Path not found: {path}"
        
        if os.path.isdir(full_path):
            import shutil
            shutil.rmtree(full_path)
            return f"Success: Deleted directory {path}"
        else:
            os.remove(full_path)
            return f"Success: Deleted file {path}"
    
    except PermissionError:
        return f"Error: Permission denied: {path}"
    except Exception as e:
        return f"Error deleting: {str(e)}"

# ========== PENTESTING TOOLS ==========

@mcp.tool()
async def run_tool(tool: str = "", arguments: str = "") -> str:
    """Run approved bug-bounty and pentesting tools with specified arguments."""
    tool = tool.strip().lower()
    if not tool:
        return "Error: Tool name is required"
    
    if tool not in SAFE_TOOLS:
        return f"Error: Tool '{tool}' is not in the approved list. Allowed tools: {', '.join(sorted(SAFE_TOOLS))}\n\nTip: Use 'search_tool' to find and 'install_tool' to add new tools."
    
    # Parse arguments
    args_list = []
    if arguments.strip():
        args_list = arguments.strip().split()
        args_list = [sanitize_input(arg) for arg in args_list]
    
    cmd = [tool] + args_list
    use_sudo = tool in SUDO_TOOLS
    
    returncode, stdout, stderr = run_command(cmd, use_sudo=use_sudo)
    
    if returncode == 0:
        return f"Tool: {tool}\nCommand: {' '.join(cmd)}\nSudo: {use_sudo}\n\nOutput:\n{stdout}"
    else:
        return f"Tool: {tool}\nCommand: {' '.join(cmd)}\nSudo: {use_sudo}\n\nError (code {returncode}):\n{stderr}\n\nOutput:\n{stdout}"

@mcp.tool()
async def nmap_scan(target: str = "", scan_type: str = "basic", ports: str = "") -> str:
    """Perform network port scanning on target host using nmap (with sudo)."""
    target = sanitize_input(target)
    if not target:
        return "Error: Valid target IP or hostname is required"
    
    scan_type = scan_type.strip().lower()
    
    if scan_type == "basic":
        cmd = ["nmap", "-sV", target]
    elif scan_type == "quick":
        cmd = ["nmap", "-F", target]
    elif scan_type == "full":
        cmd = ["nmap", "-p-", target]
    elif scan_type == "service":
        cmd = ["nmap", "-sV", "-sC", target]
    else:
        cmd = ["nmap", "-sV", target]
    
    if ports.strip():
        ports_clean = re.sub(r'[^0-9,-]', '', ports.strip())
        if ports_clean:
            cmd.extend(["-p", ports_clean])
    
    # Use sudo for nmap
    returncode, stdout, stderr = run_command(cmd, use_sudo=True, timeout=900)
    
    if returncode == 0:
        return f"Nmap Scan Results for {target}:\n\n{stdout}"
    else:
        return f"Nmap scan failed:\n{stderr}\n\nOutput:\n{stdout}"

@mcp.tool()
async def nikto_scan(target: str = "") -> str:
    """Scan web server for vulnerabilities using nikto (with sudo)."""
    target = sanitize_input(target)
    if not target:
        return "Error: Valid target URL or hostname is required"
    
    if not target.startswith(('http://', 'https://')):
        target = f"http://{target}"
    
    cmd = ["nikto", "-h", target, "-Format", "txt"]
    
    returncode, stdout, stderr = run_command(cmd, timeout=600, use_sudo=True)
    
    if returncode == 0 or stdout:
        return f"Nikto Scan Results for {target}:\n\n{stdout}"
    else:
        return f"Nikto scan failed:\n{stderr}"

@mcp.tool()
async def ffuf_scan(url: str = "", wordlist: str = "common") -> str:
    """Fast web fuzzer for directory and parameter discovery."""
    url = sanitize_input(url)
    if not url:
        return "Error: Valid URL is required"
    
    if "FUZZ" not in url:
        if url.endswith('/'):
            url = url + "FUZZ"
        else:
            url = url + "/FUZZ"
    
    if wordlist == "common":
        wordlist_path = "/usr/share/wordlists/dirb/common.txt"
    else:
        wordlist_path = "/usr/share/wordlists/dirb/big.txt"
    
    cmd = ["ffuf", "-u", url, "-w", wordlist_path, "-mc", "200,301,302,403"]
    
    returncode, stdout, stderr = run_command(cmd, timeout=600)
    
    if returncode == 0:
        return f"FFUF Results:\n\n{stdout}"
    else:
        return f"FFUF scan failed:\n{stderr}"

@mcp.tool()
async def sqlmap_test(url: str = "", data: str = "") -> str:
    """Test web application for SQL injection vulnerabilities using sqlmap (with sudo)."""
    url = sanitize_input(url)
    if not url:
        return "Error: Valid URL is required"
    
    cmd = ["sqlmap", "-u", url, "--batch", "--risk=1", "--level=1"]
    
    if data.strip():
        cmd.extend(["--data", sanitize_input(data)])
    
    returncode, stdout, stderr = run_command(cmd, timeout=600, use_sudo=True)
    
    if returncode == 0 or stdout:
        return f"SQLMap Results for {url}:\n\n{stdout}"
    else:
        return f"SQLMap failed:\n{stderr}"

@mcp.tool()
async def nuclei_scan(target: str = "", templates: str = "default") -> str:
    """Fast vulnerability scanner using nuclei templates (with sudo)."""
    target = sanitize_input(target)
    if not target:
        return "Error: Valid target is required"
    
    cmd = ["nuclei", "-u", target, "-silent"]
    
    if templates.strip() and templates != "default":
        cmd.extend(["-t", sanitize_input(templates)])
    
    returncode, stdout, stderr = run_command(cmd, timeout=600, use_sudo=True)
    
    if returncode == 0 or stdout:
        return f"Nuclei Scan Results:\n\n{stdout}"
    else:
        return f"Nuclei scan failed:\n{stderr}"

@mcp.tool()
async def whatweb_scan(target: str = "") -> str:
    """Identify web technologies and frameworks."""
    target = sanitize_input(target)
    if not target:
        return "Error: Valid target is required"
    
    if not target.startswith(('http://', 'https://')):
        target = f"http://{target}"
    
    cmd = ["whatweb", target]
    
    returncode, stdout, stderr = run_command(cmd)
    
    if returncode == 0:
        return f"WhatWeb Results:\n\n{stdout}"
    else:
        return f"WhatWeb failed:\n{stderr}"

# === SERVER STARTUP ===
if __name__ == "__main__":
    # Run the server without any logging output
    mcp.run(transport='stdio')
