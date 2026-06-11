import os
import sys
import json
import argparse
from datetime import datetime

def parse_args():
    parser = argparse.ArgumentParser(description="Extract user feedback and errors from Antigravity conversation log.")
    parser.add_argument("--app-data-dir", default=os.path.expanduser("~/.gemini/antigravity-ide"), help="Path to the app data folder")
    parser.add_argument("--conv-id", required=True, help="Active conversation ID")
    parser.add_argument("--output", default=None, help="Output file path")
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Resolve paths
    log_path = os.path.join(args.app_data_dir, "brain", args.conv_id, ".system_generated", "logs", "transcript.jsonl")
    log_path = os.path.abspath(log_path)
    
    if not os.path.exists(log_path):
        print(f"Error: Transcript log file not found at: {log_path}", file=sys.stderr)
        sys.exit(1)
        
    if args.output:
        out_path = os.path.abspath(args.output)
    else:
        # Default to workspace scratch folder
        script_dir = os.path.dirname(os.path.abspath(__file__))
        out_path = os.path.join(os.path.dirname(script_dir), "scratch", "feedback_summary.txt")
        
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    
    print(f"Reading transcript logs from: {log_path}")
    
    feedback_entries = []
    
    with open(log_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                step_idx = data.get("step_index", line_num)
                source = data.get("source", "")
                step_type = data.get("type", "")
                status = data.get("status", "")
                content = data.get("content", "")
                
                # Check for user input or errors
                if step_type == "USER_INPUT" or source == "USER_EXPLICIT":
                    feedback_entries.append({
                        "step": step_idx,
                        "type": "USER_INPUT",
                        "content": content
                    })
                elif status == "ERROR":
                    # Capture failed tool calls or execution errors
                    tool_calls = data.get("tool_calls", [])
                    tool_desc = ""
                    if tool_calls:
                        tool_desc = f" | Tool: {tool_calls[0].get('name', '')} (Args: {json.dumps(tool_calls[0].get('arguments', {}))})"
                    feedback_entries.append({
                        "step": step_idx,
                        "type": "SYSTEM_ERROR",
                        "content": f"Step failed with status ERROR{tool_desc}. Detail: {content}"
                    })
            except json.JSONDecodeError:
                continue

    # Write summary
    with open(out_path, "w", encoding="utf-8") as out:
        out.write("==================================================\n")
        out.write("CONVERSATION FEEDBACK & ERROR SUMMARY LOG\n")
        out.write(f"Generated at: {datetime.now().isoformat()}\n")
        out.write(f"Conversation ID: {args.conv_id}\n")
        out.write("==================================================\n\n")
        
        if not feedback_entries:
            out.write("No feedback entries or errors detected.\n")
        else:
            for entry in feedback_entries:
                out.write(f"--- [Step {entry['step']}] [{entry['type']}] ---\n")
                out.write(f"{entry['content'].strip()}\n\n")
                
    print(f"Extracted {len(feedback_entries)} entries successfully to: {out_path}")

if __name__ == "__main__":
    main()
