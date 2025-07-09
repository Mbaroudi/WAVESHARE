#!/usr/bin/env python3
"""
Waveshare CAN Tool - Web Interface
Browser-based configuration tool
"""

import http.server
import socketserver
import json
import urllib.parse
import threading
import webbrowser
import time
from waveshare_can_tool import WaveshareCANTool, WorkMode, FrameType


class WebInterface:
    def __init__(self, port=8080):
        self.port = port
        self.tool = WaveshareCANTool()
        self.server = None
        self.running = False
        
    def get_html_page(self):
        """Generate HTML page"""
        return """
<!DOCTYPE html>
<html>
<head>
    <title>Waveshare CAN Tool</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        .section { margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
        .form-group { margin: 10px 0; }
        label { display: inline-block; width: 150px; }
        input, select, button { margin: 5px; padding: 5px; }
        button { background: #007cba; color: white; border: none; padding: 8px 16px; cursor: pointer; }
        button:hover { background: #005a8b; }
        .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
        .success { background: #d4edda; color: #155724; }
        .error { background: #f8d7da; color: #721c24; }
        .log { background: #f8f9fa; padding: 10px; font-family: monospace; max-height: 300px; overflow-y: auto; }
        .tabs { margin: 20px 0; }
        .tab { background: #f1f1f1; padding: 10px 20px; margin: 0 2px; cursor: pointer; display: inline-block; }
        .tab.active { background: #007cba; color: white; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Waveshare CAN Tool - Web Interface</h1>
        
        <div class="section">
            <h2>Connection</h2>
            <div class="form-group">
                <label>Serial Port:</label>
                <input type="text" id="port" value="/dev/tty.usbserial-1140">
                <button onclick="connectDevice()">Connect</button>
                <button onclick="disconnectDevice()">Disconnect</button>
            </div>
            <div id="connection-status" class="status"></div>
        </div>

        <div class="tabs">
            <div class="tab active" onclick="showTab('config')">Configuration</div>
            <div class="tab" onclick="showTab('monitor')">Monitor</div>
            <div class="tab" onclick="showTab('test')">Test</div>
        </div>

        <div id="config" class="tab-content active">
            <div class="section">
                <h3>UART Settings</h3>
                <div class="form-group">
                    <label>Baud Rate:</label>
                    <select id="uart_baud">
                        <option value="9600">9600</option>
                        <option value="19200">19200</option>
                        <option value="38400">38400</option>
                        <option value="57600">57600</option>
                        <option value="115200" selected>115200</option>
                        <option value="230400">230400</option>
                        <option value="460800">460800</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Data Bits:</label>
                    <select id="uart_data">
                        <option value="7">7</option>
                        <option value="8" selected>8</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Stop Bits:</label>
                    <select id="uart_stop">
                        <option value="1" selected>1</option>
                        <option value="2">2</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Parity:</label>
                    <select id="uart_parity">
                        <option value="N" selected>None</option>
                        <option value="E">Even</option>
                        <option value="O">Odd</option>
                    </select>
                </div>
            </div>

            <div class="section">
                <h3>CAN Settings</h3>
                <div class="form-group">
                    <label>CAN Baud Rate:</label>
                    <select id="can_baud">
                        <option value="10000">10k</option>
                        <option value="20000">20k</option>
                        <option value="50000">50k</option>
                        <option value="100000">100k</option>
                        <option value="125000">125k</option>
                        <option value="250000">250k</option>
                        <option value="500000" selected>500k</option>
                        <option value="1000000">1M</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Frame Type:</label>
                    <select id="can_frame">
                        <option value="standard" selected>Standard</option>
                        <option value="extended">Extended</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Work Mode:</label>
                    <select id="work_mode">
                        <option value="1" selected>Transparent</option>
                        <option value="2">Transparent with ID</option>
                        <option value="3">Format Conversion</option>
                        <option value="4">Modbus RTU</option>
                    </select>
                </div>
                <button onclick="applyConfig()">Apply Configuration</button>
                <button onclick="resetDevice()">Reset Device</button>
            </div>
        </div>

        <div id="monitor" class="tab-content">
            <div class="section">
                <h3>CAN Monitor</h3>
                <button onclick="startMonitor()">Start Monitor</button>
                <button onclick="stopMonitor()">Stop Monitor</button>
                <button onclick="clearLog()">Clear Log</button>
                <div id="monitor-log" class="log"></div>
            </div>
        </div>

        <div id="test" class="tab-content">
            <div class="section">
                <h3>Send CAN Frame</h3>
                <div class="form-group">
                    <label>CAN ID:</label>
                    <input type="text" id="test_id" value="0x123">
                </div>
                <div class="form-group">
                    <label>Data (hex):</label>
                    <input type="text" id="test_data" value="01 02 03 04 05 06 07 08">
                </div>
                <button onclick="sendFrame()">Send Frame</button>
            </div>
        </div>

        <div id="status" class="status"></div>
    </div>

    <script>
        let connected = false;
        let monitoring = false;

        function showTab(tabName) {
            // Hide all tab contents
            const contents = document.querySelectorAll('.tab-content');
            contents.forEach(content => content.classList.remove('active'));
            
            // Remove active class from all tabs
            const tabs = document.querySelectorAll('.tab');
            tabs.forEach(tab => tab.classList.remove('active'));
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }

        function showStatus(message, isError = false) {
            const status = document.getElementById('status');
            status.textContent = message;
            status.className = isError ? 'status error' : 'status success';
        }

        function connectDevice() {
            const port = document.getElementById('port').value;
            fetch('/api/connect', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({port: port})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    connected = true;
                    showStatus('Connected to ' + port);
                    document.getElementById('connection-status').innerHTML = 
                        '<span style="color: green;">Connected</span>';
                } else {
                    showStatus('Connection failed: ' + data.error, true);
                }
            })
            .catch(error => showStatus('Error: ' + error, true));
        }

        function disconnectDevice() {
            fetch('/api/disconnect', {method: 'POST'})
            .then(response => response.json())
            .then(data => {
                connected = false;
                showStatus('Disconnected');
                document.getElementById('connection-status').innerHTML = 
                    '<span style="color: red;">Disconnected</span>';
            });
        }

        function applyConfig() {
            if (!connected) {
                showStatus('Please connect first', true);
                return;
            }

            const config = {
                uart_baud: parseInt(document.getElementById('uart_baud').value),
                uart_data: parseInt(document.getElementById('uart_data').value),
                uart_stop: parseInt(document.getElementById('uart_stop').value),
                uart_parity: document.getElementById('uart_parity').value,
                can_baud: parseInt(document.getElementById('can_baud').value),
                can_frame: document.getElementById('can_frame').value,
                work_mode: parseInt(document.getElementById('work_mode').value)
            };

            fetch('/api/config', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(config)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showStatus('Configuration applied');
                } else {
                    showStatus('Configuration failed: ' + data.error, true);
                }
            })
            .catch(error => showStatus('Error: ' + error, true));
        }

        function resetDevice() {
            if (!connected) {
                showStatus('Please connect first', true);
                return;
            }

            if (confirm('Are you sure you want to reset the device?')) {
                fetch('/api/reset', {method: 'POST'})
                .then(response => response.json())
                .then(data => showStatus('Device reset'));
            }
        }

        function startMonitor() {
            if (!connected) {
                showStatus('Please connect first', true);
                return;
            }

            monitoring = true;
            fetch('/api/monitor/start', {method: 'POST'})
            .then(response => response.json())
            .then(data => {
                showStatus('Monitoring started');
                pollMonitorData();
            });
        }

        function stopMonitor() {
            monitoring = false;
            fetch('/api/monitor/stop', {method: 'POST'})
            .then(response => response.json())
            .then(data => showStatus('Monitoring stopped'));
        }

        function clearLog() {
            document.getElementById('monitor-log').innerHTML = '';
        }

        function pollMonitorData() {
            if (!monitoring) return;

            fetch('/api/monitor/data')
            .then(response => response.json())
            .then(data => {
                if (data.data) {
                    const log = document.getElementById('monitor-log');
                    data.data.forEach(line => {
                        log.innerHTML += line + '<br>';
                    });
                    log.scrollTop = log.scrollHeight;
                }
                if (monitoring) {
                    setTimeout(pollMonitorData, 1000);
                }
            })
            .catch(error => {
                if (monitoring) {
                    setTimeout(pollMonitorData, 1000);
                }
            });
        }

        function sendFrame() {
            if (!connected) {
                showStatus('Please connect first', true);
                return;
            }

            const id = document.getElementById('test_id').value;
            const data = document.getElementById('test_data').value;

            fetch('/api/send', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({id: id, data: data})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showStatus('Frame sent');
                } else {
                    showStatus('Send failed: ' + data.error, true);
                }
            })
            .catch(error => showStatus('Error: ' + error, true));
        }
    </script>
</body>
</html>
"""

    def handle_api_request(self, path, method, data):
        """Handle API requests"""
        try:
            if path == '/api/connect':
                port = data.get('port', '/dev/tty.usbserial-1140')
                self.tool.port = port
                success = self.tool.connect()
                return {'success': success, 'error': None if success else 'Connection failed'}
            
            elif path == '/api/disconnect':
                self.tool.disconnect()
                return {'success': True}
            
            elif path == '/api/config':
                # Apply configuration
                self.tool.config.uart_baud = data['uart_baud']
                self.tool.config.uart_data_bits = data['uart_data']
                self.tool.config.uart_stop_bits = data['uart_stop']
                self.tool.config.uart_parity = data['uart_parity']
                self.tool.config.can_baud = data['can_baud']
                self.tool.config.can_frame_type = FrameType.STANDARD if data['can_frame'] == 'standard' else FrameType.EXTENDED
                self.tool.config.work_mode = WorkMode(data['work_mode'])
                
                success = self.tool.apply_config()
                return {'success': success, 'error': None if success else 'Config failed'}
            
            elif path == '/api/reset':
                self.tool.reset_device()
                return {'success': True}
            
            elif path == '/api/monitor/start':
                self.tool.start_monitoring()
                return {'success': True}
            
            elif path == '/api/monitor/stop':
                self.tool.stop_monitoring()
                return {'success': True}
            
            elif path == '/api/monitor/data':
                # Return mock data for now
                return {'data': []}
            
            elif path == '/api/send':
                can_id = int(data['id'], 16)
                frame_data = bytes.fromhex(data['data'].replace(' ', ''))
                success = self.tool.send_can_frame(can_id, frame_data)
                return {'success': success, 'error': None if success else 'Send failed'}
            
            else:
                return {'success': False, 'error': 'Unknown endpoint'}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def run(self):
        """Run the web server"""
        class RequestHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                self.web_interface = kwargs.pop('web_interface')
                super().__init__(*args, **kwargs)
            
            def do_GET(self):
                if self.path == '/':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(self.web_interface.get_html_page().encode())
                else:
                    super().do_GET()
            
            def do_POST(self):
                if self.path.startswith('/api/'):
                    content_length = int(self.headers.get('Content-Length', 0))
                    post_data = self.rfile.read(content_length)
                    
                    try:
                        data = json.loads(post_data.decode()) if post_data else {}
                    except:
                        data = {}
                    
                    response = self.web_interface.handle_api_request(self.path, 'POST', data)
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode())
                else:
                    super().do_POST()
        
        handler = lambda *args, **kwargs: RequestHandler(*args, web_interface=self, **kwargs)
        
        self.server = socketserver.TCPServer(("", self.port), handler)
        self.running = True
        
        print(f"Web interface running at: http://localhost:{self.port}")
        print("Press Ctrl+C to stop")
        
        # Open browser
        webbrowser.open(f"http://localhost:{self.port}")
        
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            self.running = False
            self.server.shutdown()
            print("\nWeb interface stopped")


def main():
    """Main function"""
    interface = WebInterface()
    interface.run()


if __name__ == "__main__":
    main()