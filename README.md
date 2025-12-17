# CipherBot2 MCP Server

A powerful Model Context Protocol (MCP) server that provides AI assistants with secure access to penetration testing tools, **dynamic package management**, and filesystem operations in a controlled Kali Linux environment.

## 🌟 Key Features

### 🤖 AI-Powered Tool Management
**CipherBot2's killer feature**: Ask the AI to install tools on-demand!

- **"Search for amass tool"** → AI searches Kali repositories
- **"Install subfinder"** → AI installs it instantly
- **"What tools can I use for subdomain enumeration?"** → AI suggests and installs them
- **No Docker rebuilds needed** → Tools are installed dynamically during conversation

### 🛠️ Pre-installed Pentesting Tools
- **Network Scanning**: nmap, masscan, rustscan
- **Web Scanning**: nikto, whatweb, ffuf, gobuster, dirb, wfuzz
- **Vulnerability Detection**: nuclei, sqlmap, xsstrike, commix
- **Reconnaissance**: amass, subfinder, assetfinder, sublist3r, dnsenum, fierce
- **Web Application Analysis**: httpx, aquatone, katana, wafw00f, joomscan

### 📦 Dynamic Package Management
- **AI-Driven Installation**: Just ask the AI to install what you need
- **Search Packages**: "Search for tools related to DNS enumeration"
- **Remove Tools**: "Uninstall nikto, I don't need it anymore"
- **Python Packages**: "Install the requests Python library"
- **List Installed**: "Show me all installed security tools"

### 📁 Filesystem Access (With Your Permission)
- **Read Files**: "Read the file at /home/user/notes.txt"
- **Write Files**: "Save this scan result to report.txt"
- **Execute Scripts**: "Run the script at /home/user/scan.sh"
- **Directory Operations**: "List files in my projects folder"
- **Safe Paths**: Automatic sanitization prevents directory traversal attacks

### 🔒 Security-First Design
- **Explicit Permissions**: Every sensitive operation requires your approval
- **Input Sanitization**: All inputs are sanitized to prevent command injection
- **Tool Whitelist**: Dynamically managed whitelist of approved tools
- **Sudo Support**: Privileged tools run with appropriate permissions
- **Isolated Environment**: Everything runs in Docker container
- **Host Filesystem Mount**: Optional mounting with granular control

---

## 📋 Prerequisites

- **Docker Engine**: Installed and running on your system
- **Docker Permissions**: Your user must be in the `docker` group (no sudo required)
- **Claude Desktop**: Installed and configured
- **Disk Space**: ~5GB for Kali Linux base image and tools
- **Internet Connection**: Required for installing tools on-demand

---

## 🚀 Quick Start Guide

### Step 1: Prepare Your Files

Make sure you have these files in your project directory:
```
/home/shadowcipher/cipherbot2/
├── Dockerfile
├── mcp_server.py
├── requirements.txt
├── run_cipherbot2.sh
└── README.md
```

### Step 2: Make Run Script Executable
```bash
cd /home/shadowcipher/cipherbot2
chmod +x run_cipherbot2.sh
```

### Step 3: Build Docker Image
```bash
docker build -t cipherbot2-mcp-server .
```

⏱️ This takes 10-15 minutes (downloads Kali Linux and installs base tools)

### Step 4: Fix Docker Permissions (If Needed)
```bash
# Add your user to docker group
sudo usermod -aG docker $USER

# IMPORTANT: Log out and back in (or reboot) for this to take effect
# Then verify it works:
docker ps  # Should work without sudo
```

### Step 5: Configure Claude Desktop

**Method A - Using Claude Desktop UI (Recommended):**
1. Open **Claude Desktop**
2. Go to **Settings** → **Developer** → **Edit Config**
3. Add this configuration:
```json
{
  "mcpServers": {
    "cipherbot2": {
      "command": "/home/shadowcipher/cipherbot2/run_cipherbot2.sh"
    }
  }
}
```

**Method B - Using Terminal:**
```bash
cat > ~/.config/Claude/config.json <<'CONFIGEOF'
{
  "mcpServers": {
    "cipherbot2": {
      "command": "/home/shadowcipher/cipherbot2/run_cipherbot2.sh"
    }
  }
}
CONFIGEOF
```

⚠️ **CRITICAL**: Replace `/home/shadowcipher/cipherbot2/run_cipherbot2.sh` with **YOUR ACTUAL FULL PATH**!

To get your path:
```bash
cd /home/shadowcipher/cipherbot2
pwd  # Copy this output
```

### Step 6: Test the Server (Optional)
```bash
./run_cipherbot2.sh
```

You should see:
```
===================================
CipherBot2 MCP Server
===================================
Mounting host path: /home/shadowcipher
Container path: /host
...
Starting CipherBot MCP server...
WARNING: This tool is for authorized security testing only!
Filesystem access base: /host
Running as: ROOT (full privileges)
```

Press **Ctrl+C** to stop the test.

### Step 7: Restart Claude Desktop

**IMPORTANT**: Fully quit Claude Desktop (not just close the window):
```bash
# On Linux
killall -9 claude-desktop claude

# Then launch Claude Desktop fresh from your application menu
```

### Step 8: Verify Connection

In Claude Desktop, ask:

**"What security tools do you have available?"**

If connected successfully, Claude will list the available tools and capabilities!

---

## 🎯 Usage Examples

### 🔍 AI-Powered Tool Installation (The Game Changer!)

**Natural Language Tool Management:**
```
You: "I need a tool for subdomain enumeration"
AI: "I can help! Let me search for subdomain tools..."
    [Searches repositories]
AI: "I found sublist3r, subfinder, and amass. Would you like me to install them?"
You: "Yes, install subfinder"
AI: [Installs subfinder]
    "Done! Subfinder is now available. Would you like me to scan a domain?"
```

**Direct Installation:**
```
"Search for amass in the repositories"
"Install amass tool"
"Install subfinder and assetfinder"
"What reconnaissance tools are available?"
"Install all common subdomain enumeration tools"
```

**Python Tools:**
```
"Install the dirsearch Python tool"
"Install requests library via pip"
"Search for Python security packages"
```

**Management:**
```
"List all installed security tools"
"Show me what packages are installed"
"Uninstall nikto, I don't need it"
"Remove wfuzz package"
```

### 🌐 Network Scanning
```
"Scan 192.168.1.1 with nmap"
"Run a quick nmap scan on localhost ports 80,443,8080"
"Perform a stealth scan on example.com"
"Scan 10.0.0.5 and show service versions"
```

### 🕷️ Web Application Testing
```
"Scan https://example.com with nikto"
"Use ffuf to fuzz directories on https://target.com/FUZZ"
"Check what technologies example.com uses"
"Test http://testsite.local for SQL injection"
"Run nuclei vulnerability scan on https://target.com"
"Check if example.com has a WAF"
```

### 🔎 Reconnaissance
```
"Find subdomains of example.com"
"Enumerate DNS records for target.com"
"Use amass to discover subdomains of example.com"
"Search for subdomains using multiple tools"
```

### 📁 Filesystem Operations
```
"Read the file /home/user/wordlist.txt"
"List all files in /home/user/reports/"
"Create a directory called scan-results"
"Save this nmap output to /home/user/scan-results/report.txt"
"Execute the scanning script at /home/user/scripts/auto-scan.sh"
"Write these findings to a file called vulnerability-report.md"
```

### 🔄 Workflow Automation
```
"Install amass, then scan example.com for subdomains, 
 then save the results to subdomains.txt"

"Search for feroxbuster, install it if found, 
 then scan https://target.com/FUZZ for directories"

"Read targets.txt, then scan each target with nmap, 
 and save results to scan-results/"
```

---

## 🏗️ Architecture
```
┌─────────────────────────────────────────────────────┐
│              Claude Desktop (You)                    │
│         "Install amass and scan example.com"        │
└────────────────────┬────────────────────────────────┘
                     │
                     │ MCP Protocol (stdio)
                     │
┌────────────────────▼────────────────────────────────┐
│              run_cipherbot2.sh                       │
│        Launches Docker Container                     │
└────────────────────┬────────────────────────────────┘
                     │
                     │ Docker Run with Mounts
                     │
┌────────────────────▼────────────────────────────────┐
│         Docker Container (Kali Linux)                │
│  ┌──────────────────────────────────────────────┐  │
│  │      CipherBot2 MCP Server (Python)          │  │
│  │  ┌────────────────────────────────────────┐  │  │
│  │  │  🔧 Tool Management                     │  │  │
│  │  │  - install_tool()                       │  │  │
│  │  │  - search_tool()                        │  │  │
│  │  │  - remove_tool()                        │  │  │
│  │  └────────────────────────────────────────┘  │  │
│  │  ┌────────────────────────────────────────┐  │  │
│  │  │  🛡️  Security Tools                     │  │  │
│  │  │  - nmap, nikto, sqlmap, nuclei...      │  │  │
│  │  │  - Dynamically installed tools          │  │  │
│  │  └────────────────────────────────────────┘  │  │
│  │  ┌────────────────────────────────────────┐  │  │
│  │  │  📁 Filesystem Access                   │  │  │
│  │  │  - Read/Write/Execute                   │  │  │
│  │  │  - Mounted at /host                     │  │  │
│  │  └────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────┘
                     │
                     │ Volume Mount (-v)
                     │
┌────────────────────▼────────────────────────────────┐
│          Host Filesystem (/home/shadowcipher)        │
│            Your files accessible at /host            │
└─────────────────────────────────────────────────────┘
```

---

## 🔒 Security Model

### Permission-Based Access Control

Every sensitive operation requires **explicit user approval** through Claude's interface:

| Operation | Requires Permission | Example |
|-----------|-------------------|---------|
| Install package | ✅ Yes | "Install amass" → You approve |
| Remove package | ✅ Yes | "Remove nikto" → You approve |
| Read file | ✅ Yes | "Read config.txt" → You approve |
| Write file | ✅ Yes | "Save to report.txt" → You approve |
| Execute script | ✅ Yes | "Run scan.sh" → You approve |
| Run approved tool | ✅ Yes | "Scan with nmap" → You approve |
| List directory | ❌ No | Read-only operation |
| Search packages | ❌ No | Read-only operation |

### Defense-in-Depth Security

1. **Input Sanitization**: All user inputs are sanitized to prevent command injection
2. **Tool Whitelist**: Only approved tools can be executed (dynamically managed)
3. **Path Sanitization**: Filesystem paths are normalized to prevent traversal attacks
4. **Container Isolation**: Everything runs inside an isolated Docker container
5. **Mounted Paths Only**: Only explicitly mounted directories are accessible
6. **No Network Bypass**: Cannot access internal networks without your permission
7. **Logging**: All operations are logged to stderr for audit trail

### Filesystem Safety
```
Host System: /home/shadowcipher/
                    ↓
            (mounted as)
                    ↓
Container:         /host/
                    ↓
            (accessed via)
                    ↓
        fs_read("/projects/file.txt")
                    ↓
        Resolves to: /host/projects/file.txt
                    ↓
        Real path: /home/shadowcipher/projects/file.txt
```

- Paths are sanitized to prevent `../../../etc/passwd` attacks
- Only mounted directory tree is accessible
- Files outside mount point cannot be accessed
- Symbolic links are handled safely

### What CipherBot2 CANNOT Do

❌ Access files outside mounted directory  
❌ Execute arbitrary system commands  
❌ Bypass Docker container isolation  
❌ Access your passwords or SSH keys (unless you explicitly mount them)  
❌ Make network requests without tool invocation  
❌ Persist data between container restarts (unless saved to /host)  
❌ Access other users' files (respects file permissions)  

---

## 🛠️ Configuration & Customization

### Customize Mounted Directory

By default, your entire home directory is mounted. To limit access:

Edit `run_cipherbot2.sh`:
```bash
# Option 1: Mount specific project directory
HOST_PATH="/home/shadowcipher/projects"

# Option 2: Mount multiple directories (requires modification)
# Add additional -v flags:
docker run -i --rm \
  -v "/home/shadowcipher/projects:/host/projects:rw" \
  -v "/home/shadowcipher/reports:/host/reports:rw" \
  ...
```

### Add Pre-installed Tools

To add tools that are always available (no installation needed):

Edit `Dockerfile`:
```dockerfile
RUN apt update && apt install -y \
    nmap \
    nikto \
    # Add your tools here:
    masscan \
    rustscan \
    sublist3r \
    && apt clean
```

Then rebuild:
```bash
docker build -t cipherbot2-mcp-server .
```

### Modify Tool Whitelist

Edit `mcp_server.py` and update the `SAFE_TOOLS` set:
```python
SAFE_TOOLS = {
    "nmap", "amass", "subfinder", 
    # Add custom tools:
    "mytool", "customscanner"
}
```

### Adjust Timeout Values

In `mcp_server.py`, modify timeouts:
```python
# For most commands
def run_command(cmd, timeout=600, use_sudo=False):  # 10 minutes

# For specific operations
@mcp.tool()
async def install_tool(package: str = "") -> str:
    returncode, stdout, stderr = run_command(
        ["apt", "install", "-y", package],
        timeout=1200  # 20 minutes for large packages
    )
```

### Change Docker Capabilities

Edit `run_cipherbot2.sh` to modify container capabilities:
```bash
docker run -i --rm \
  --cap-add=NET_RAW \      # For raw packet access
  --cap-add=NET_ADMIN \    # For network administration
  --cap-add=SYS_ADMIN \    # Add if needed (use cautiously!)
  ...
```

---

## 🐛 Troubleshooting

### Issue: "Server Disconnected" in Claude Desktop

**Symptoms**: Claude shows "Server Disconnected" error

**Causes & Solutions**:

1. **Docker Permission Issue**
```bash
   # Check if Docker works without sudo
   docker ps
   
   # If it asks for password, fix permissions:
   sudo usermod -aG docker $USER
   # Then MUST log out and back in (or reboot)
```

2. **Docker Image Not Built**
```bash
   # Check if image exists
   docker images | grep cipherbot2
   
   # If not found, build it:
   docker build -t cipherbot2-mcp-server .
```

3. **Wrong Path in Config**
```bash
   # Verify the path in Claude config matches reality
   cat ~/.config/Claude/config.json
   ls -la /home/shadowcipher/cipherbot2/run_cipherbot2.sh
```

4. **Script Not Executable**
```bash
   chmod +x /home/shadowcipher/cipherbot2/run_cipherbot2.sh
```

### Issue: Tools Not Appearing in Claude

**Solution Steps**:

1. Verify config is correct:
```bash
   cat ~/.config/Claude/config.json
```

2. Check the path is absolute (starts with `/`):
```json
   "command": "/home/shadowcipher/cipherbot2/run_cipherbot2.sh"
   NOT: "~/cipherbot2/run_cipherbot2.sh"
   NOT: "cipherbot2/run_cipherbot2.sh"
```

3. **Fully restart Claude Desktop** (kill process, don't just close window):
```bash
   killall -9 claude-desktop claude
   # Then launch fresh from application menu
```

4. Check Claude Desktop developer logs:
   - Settings → Developer → View Logs
   - Look for errors mentioning "cipherbot2"

### Issue: "Module 'mcp' Not Found"

**Cause**: Python package missing in container

**Solution**:
```bash
# Rebuild Docker image (this reinstalls Python packages)
docker build -t cipherbot2-mcp-server .
```

### Issue: "Permission Denied" for Filesystem Operations

**Causes & Solutions**:

1. **File ownership on host**:
```bash
   # Check file permissions
   ls -la /home/shadowcipher/path/to/file
   
   # Fix if needed
   chmod 644 /home/shadowcipher/path/to/file  # For reading
   chmod 755 /home/shadowcipher/path/to/script  # For executing
```

2. **Directory not mounted**:
   - Check `run_cipherbot2.sh` to see what's mounted
   - Default: `$HOME` (your home directory)
   - Files outside this path cannot be accessed

3. **SELinux/AppArmor restrictions** (advanced):
```bash
   # Check SELinux status
   sestatus
   
   # If enforcing, may need to adjust policies
```

### Issue: "Tool Not in Approved List"

**This is normal!** You need to install the tool first:
```
You: "Run amass on example.com"
AI: "Error: Tool 'amass' is not in the approved list. Would you like me to search for and install it?"
You: "Yes, install amass"
AI: [Installs amass]
    "Done! Now I can use amass. Let me scan example.com..."
```

### Issue: Installation Fails

**Common causes**:

1. **Package name wrong**:
```
   "Search for the correct package name first"
   "Install subfinder"  # Correct
   "Install sub-finder" # Wrong (hyphen)
```

2. **Package not in Kali repos**:
```
   "Search for tool-name"
   # If not found in Kali repos, may need to install from source
```

3. **Network issues**:
```bash
   # Check container can reach internet
   docker run -it --rm cipherbot2-mcp-server ping -c 3 8.8.8.8
```

### Issue: High CPU/Memory Usage

**Cause**: Scans running in background

**Solutions**:
```bash
# View running containers
docker ps

# Stop specific container
docker stop [container-id]

# Stop all cipherbot containers
docker stop $(docker ps -q --filter ancestor=cipherbot2-mcp-server)

# Clean up stopped containers
docker container prune
```

### Issue: Slow Tool Installation

**Normal behavior**: Some tools are large and take time.

**Monitor progress**:
```bash
# In another terminal, watch Docker logs
docker logs -f [container-id]
```

**Speed up**:
```bash
# Install multiple tools at once
"Install amass subfinder assetfinder"
# Better than installing one-by-one
```

### Issue: JSON Syntax Error in Claude Config

**Symptoms**: Claude Desktop shows "Unexpected token" error

**Solution**:
```bash
# Validate JSON syntax
cat ~/.config/Claude/config.json | python3 -m json.tool

# Common mistakes:
# ❌ Extra comma: "command": "/path/to/script",}
# ❌ Missing quotes: command: /path/to/script
# ❌ Comments: // This is not allowed in JSON
# ✅ Correct:
{
  "mcpServers": {
    "cipherbot2": {
      "command": "/home/shadowcipher/cipherbot2/run_cipherbot2.sh"
    }
  }
}
```

---

## 📊 Tool Categories & Installation Guide

### 🔍 Reconnaissance Tools

**Subdomain Enumeration:**
```
"Install amass"        # Active & passive subdomain discovery
"Install subfinder"    # Fast passive subdomain discovery
"Install assetfinder"  # Find domains and subdomains
"Install sublist3r"    # Uses multiple search engines
```

**DNS Enumeration:**
```
"Install fierce"       # DNS reconnaissance
"Install dnsenum"      # DNS enumeration tool
"Install dnsrecon"     # DNS enumeration and scanning
```

**Network Discovery:**
```
"Install masscan"      # Fast port scanner
"Install rustscan"     # Modern fast port scanner
"Install zmap"         # Network scanner
```

### 🕷️ Web Application Testing

**Directory/File Discovery:**
```
"Install feroxbuster"  # Fast content discovery (Rust)
"Install dirsearch"    # Web path scanner (Python)
"Install gobuster"     # Directory/DNS bruteforcing
```

**Web Fuzzing:**
```
"Install ffuf"         # Fast web fuzzer
"Install wfuzz"        # Web application fuzzer
```

**Web Scanning:**
```
"Install whatweb"      # Web technology fingerprinting
"Install wafw00f"      # WAF detection
"Install nikto"        # Web server scanner
```

### 🛡️ Vulnerability Scanning

**Multi-Purpose:**
```
"Install nuclei"       # Template-based scanning
"Install nmap"         # Network scanner
```

**Specific Vulnerabilities:**
```
"Install sqlmap"       # SQL injection
"Install xsstrike"     # XSS detection
"Install commix"       # Command injection
```

**CMS-Specific:**
```
"Install wpscan"       # WordPress scanner
"Install joomscan"     # Joomla scanner
"Install droopescan"   # Drupal scanner
```

### 🔐 Exploitation & Post-Exploitation
```
"Install metasploit-framework"  # Exploitation framework
"Install searchsploit"          # Exploit database search
"Install exploitdb"             # Exploit database
```

### 📡 Network Analysis
```
"Install wireshark"    # Packet analyzer
"Install tcpdump"      # Packet capture
"Install netcat"       # Network Swiss Army knife
```

### 🐍 Python Security Tools
```
"Install dirsearch via pip"
"Install impacket via pip"
"Install scapy via pip"
```

---

## 🎓 Best Practices

### 1. Start with Reconnaissance
```
workflow:
1. "Install and use amass to find subdomains of target.com"
2. "Save the subdomains to targets.txt"
3. "Install httpx and check which subdomains are alive"
4. "Save alive hosts to alive.txt"
5. "Use nuclei to scan the alive hosts for vulnerabilities"
```

### 2. Use Tool Chaining
```
"Install subfinder, then find subdomains of example.com, 
 then install httpx and check which are alive,
 then save results to subdomains-alive.txt"
```

### 3. Document Everything
```
"Create a directory called target-scan-2024-12-11"
"Run nmap scan on target.com and save to target-scan-2024-12-11/nmap.txt"
"Scan with nikto and append to target-scan-2024-12-11/findings.txt"
```

### 4. Install Tools as Needed

Don't pre-install everything. Install tools when you need them:
```
"I need to test for SQL injection. What tool should I use and can you install it?"
```

### 5. Verify Before Large Scans
```
"Install masscan"
"Test masscan on localhost first"
"Now scan the production target"
```

### 6. Clean Up
```
"Show me all installed tools"
"Remove tools I don't need: wfuzz, dirsearch"
"This frees up space for new tools"
```

---

## ⚠️ Legal & Ethical Use

### ✅ AUTHORIZED USE ONLY

This tool is designed for:
- **Authorized penetration testing** with written permission
- **Bug bounty programs** within defined scope
- **Your own systems** and infrastructure
- **Educational labs** and practice environments
- **Security research** on authorized targets

### ❌ NEVER USE FOR:

- Unauthorized network scanning or reconnaissance
- Attacking systems without explicit permission
- Violating terms of service or acceptable use policies
- Any illegal activities
- Testing production systems without approval
- Compromising others' security or privacy

### 📋 Your Responsibilities

1. **Get Written Permission**: Always obtain explicit authorization before testing
2. **Follow Scope**: Stay within the defined testing scope
3. **Respect Rate Limits**: Don't DoS targets with aggressive scans
4. **Document Authorization**: Keep records of all permissions
5. **Report Responsibly**: Follow responsible disclosure practices
6. **Know the Law**: Understand applicable laws in your jurisdiction
7. **Use VPN/Authorization**: Some bug bounty programs require specific network routes

### ⚖️ Legal Disclaimer

**Unauthorized access to computer systems is illegal in most jurisdictions.**

Examples of illegal acts:
- Scanning networks without permission (can be charged as attempted hacking)
- Accessing systems beyond your authorization level
- Using tools to bypass security controls without permission
- Denial of service attacks
- Data exfiltration without authorization

**The developers and contributors of CipherBot2 are not responsible for misuse of this tool. Users are solely responsible for ensuring their use complies with all applicable laws and regulations.**

---

## 🔧 Advanced Usage

### Creating Custom Workflows
```python
# Example: Create a custom recon workflow

You: "Let's create a full reconnaissance workflow for example.com"

AI: "I'll help you set up a comprehensive recon workflow:

1. First, I'll install the necessary tools
2. Then run subdomain enumeration
3. Check which hosts are alive
4. Scan for open ports
5. Identify web technologies
6. Check for common vulnerabilities
7. Save all results organized by date

Shall I proceed?"

You: "Yes, do it"

AI: [Executes full workflow with progress updates]
```

### Integrating with External Tools
```bash
# Use CipherBot2 output with external tools

1. "Scan example.com and save results to scan.txt"
2. Exit Claude, process scan.txt with your own scripts
3. Return to Claude: "Read processed-targets.txt and scan each target"
```

### Automating Reports
```
"Scan target.com with nmap, nikto, and nuclei.
 Combine all results into a markdown report
 with sections for each tool.
 Save to report-2024-12-11.md"
```

---

## 🎯 Real-World Scenarios

### Scenario 1: Bug Bounty Reconnaissance
```
You: "I'm doing recon on example.com for a bug bounty. Help me find attack surface."

AI: "I'll help with your bug bounty recon. Let me:
     1. Install subdomain enumeration tools
     2. Find all subdomains
     3. Check which are alive
     4. Identify technologies
     5. Look for interesting endpoints
     
     Starting with subdomain enumeration..."

[AI installs amass, subfinder, runs scans, provides results]
```

### Scenario 2: Internal Network Assessment
```
You: "I need to assess our internal network 10.0.0.0/24"

AI: "I'll perform an internal network assessment:
     1. Install masscan for fast scanning
     2. Identify all hosts
     3. Scan for open services
     4. Check for common vulnerabilities
     5. Generate a report
     
     Beginning host discovery..."
```

### Scenario 3: Web Application Testing
```
You: "Test https://test.example.com for vulnerabilities"

AI: "I'll perform a web application security test:
     1. Technology fingerprinting
     2. Directory enumeration
     3. Check for SQL injection
     4. Test for XSS
     5. Scan with nuclei templates
     
     Starting with technology identification..."
```

---

## 📝 License

MIT License - Use responsibly and ethically.
```
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED. See full license text for details.
```

---

## 🤝 Contributing

Contributions are welcome! Here's how to contribute:

### Adding New Tools

1. Fork the repository
2. Add tool to `SAFE_TOOLS` in `mcp_server.py`
3. Test thoroughly in isolated environment
4. Create pull request with:
   - Tool description
   - Usage examples
   - Security considerations

### Improving Features

1. Identify improvement area
2. Implement changes
3. Test extensively
4. Document new behavior
5. Submit pull request

### Reporting Issues

When reporting issues, include:
- Operating system and version
- Docker version
- Claude Desktop version
- Steps to reproduce
- Error messages and logs
- Expected vs actual behavior

---

## 📞 Support & Community

### Getting Help

1. **Check Troubleshooting Section**: Most common issues are covered
2. **Review Examples**: See usage examples for your use case
3. **Check Logs**: Docker and Claude Desktop logs often reveal issues
4. **Test Manually**: Run `./run_cipherbot2.sh` to see errors directly

### Frequently Asked Questions

**Q: Can I use this on Windows/Mac?**  
A: Yes! Paths will differ:
- Windows: `C:\\Users\\YourName\\cipherbot2\\run_cipherbot2.sh`
- Mac: `/Users/YourName/cipherbot2/run_cipherbot2.sh`

**Q: How do I update installed tools?**  
A: Ask Claude: "Update all installed packages with apt upgrade"

**Q: Can I run multiple instances?**  
A: Yes, give each a unique name in Claude config:
```json
{
  "mcpServers": {
    "cipherbot2-primary": {"command": "/path/to/script1.sh"},
    "cipherbot2-secondary": {"command": "/path/to/script2.sh"}
  }
}
```

**Q: Is my data safe?**  
A: Yes. Data never leaves your machine. Only mounted directories are accessible.

**Q: Can tools be malicious?**  
A: Only install tools from official Kali repositories. Don't install random packages.

