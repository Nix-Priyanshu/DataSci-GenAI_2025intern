def get_recent_history(messages, limit=6):
    if not messages:
        return ""
    
    recent = messages[-limit:]
    return "\n".join(f"{m['role']}: {m['content']}" for m in recent)
