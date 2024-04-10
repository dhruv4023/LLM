MESSAGES = {
    # Bot messages
    2000: "Answered successfully.",
    2001: "Temporary chain created successfully.Will be deleted after 2 hours.",
    2002: "Embedding added successfully.",
    2003: "No files provided",
    2004: "Unsupported file format",
    # Chat messages
    3000: "Chat created successfully.",
    3001: "Chats fetched successfully.",
    3002: "Chat fetched successfully.",
    3003: "Chat not found.",
    3004: "Chat updated successfully.",
    3005: "Chat deleted successfully.",
    3006: "Chat with this collection name already exists.",
    3007: "Icon file must be uploaded.",
    # Chat history messages
    4000: "Chat history created successfully.",
    4001: "Chat history retrieved successfully.",
    4002: "Chat history not found.",
    4003: "Chat history updated successfully.",
    4004: "Chat history deleted successfully.",
    4005: "Question deleted successfully.",
    4006: "Question not found.",
    # Authorization messages
    5001: "Unauthorized - Admin access required.",
    5002: "Access denied - Unauthorized.",
    5003: "Your session expired! Please log in again.",
    # General messages
    9000: "Chatbot API server is running...",
    9999: "Internal Server Error.",
}


def get_message(message_code):
    if isinstance(message_code, int) and message_code in MESSAGES:
        return MESSAGES[message_code]

    return message_code
