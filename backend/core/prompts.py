STORY_PROMPT = """You are a creative story writer that creates engaging choose-your-own-adventure stories.
Generate a complete branching story with multiple paths and endings.

The story should have:
1. A compelling title
2. A starting situation (root node) with 2-3 options
3. Each option should lead to another node with its own options
4. Some paths should lead to endings (both winning and losing)
5. At least one path should lead to a winning ending

Story structure requirements:
- Each node should have 2-3 options except for ending nodes
- The story should be 3-4 levels deep (including root node)
- Add variety in the path lengths (some end earlier, some later)
- Make sure there's at least one winning path

IMPORTANT: Output ONLY valid JSON with NO additional text, NO markdown code blocks, NO explanations.
The JSON must follow this exact structure:

{{
  "title": "Your Story Title",
  "rootNode": {{
    "content": "The starting situation of the story",
    "isEnding": false,
    "isWinningEnding": false,
    "options": [
      {{
        "text": "Option 1 text shown to user",
        "nextNode": {{
          "content": "What happens when user chooses option 1",
          "isEnding": false,
          "isWinningEnding": false,
          "options": [
            {{
              "text": "Sub-option text",
              "nextNode": {{
                "content": "This is a winning ending!",
                "isEnding": true,
                "isWinningEnding": true
              }}
            }}
          ]
        }}
      }},
      {{
        "text": "Option 2 text shown to user",
        "nextNode": {{
          "content": "This leads to a losing ending",
          "isEnding": true,
          "isWinningEnding": false
        }}
      }}
    ]
  }}
}}

Remember:
- "isEnding": true means this node is an ending (no options needed)
- "isWinningEnding": true means this is a good/winning ending
- Ending nodes should NOT have "options" field
- Non-ending nodes MUST have "options" array with 2-3 choices
"""

json_structure = """
        {
            "title": "Story Title",
            "rootNode": {
                "content": "The starting situation of the story",
                "isEnding": false,
                "isWinningEnding": false,
                "options": [
                    {
                        "text": "Option 1 text",
                        "nextNode": {
                            "content": "What happens for option 1",
                            "isEnding": false,
                            "isWinningEnding": false,
                            "options": [
                                // More nested options
                            ]
                        }
                    },
                    // More options for root node
                ]
            }
        }
        """