#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(__file__))

from python.helpers.mcp_handler import MCPConfig

def count_mcp_tools(mcp_servers_config: str):
    try:
        MCPConfig.update(mcp_servers_config)
        tools = MCPConfig.get_instance().get_tools()
        total_tools = len(tools)
        print(f"Total MCP tools: {total_tools}")
        
        # Count per server
        server_counts = {}
        for tool in tools:
            for key, value in tool.items():
                server_name = value.get('server', 'unknown')
                if server_name not in server_counts:
                    server_counts[server_name] = 0
                server_counts[server_name] += 1
        
        print("Tools per server:")
        for server, count in server_counts.items():
            print(f"  {server}: {count}")
        
        return total_tools
    except Exception as e:
        print(f"Error: {e}")
        return 0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python count_mcp_tools.py '<mcp_servers_json_string>'")
        sys.exit(1)
    
    config_str = sys.argv[1]
    count_mcp_tools(config_str)