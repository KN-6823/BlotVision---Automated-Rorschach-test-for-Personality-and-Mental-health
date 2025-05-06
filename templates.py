# templates.py

personality_templates = {
    "positive": [
        "You approach life with optimism, always seeing potential and possibility in every situation.",
        "Your positive outlook shines through, even in the face of challenges.",
        "Your enthusiasm and drive to succeed motivate others around you.",
        "You focus on finding solutions instead of problems, helping others follow your example.",
        "Your bright energy brings hope and a sense of possibility to all those around you."
    ],
    "negative": [
        "You may have a cautious nature, often anticipating challenges and preparing for worst-case scenarios.",
        "Your tendency to focus on the negatives might make it hard for you to enjoy the present.",
        "You sometimes find it difficult to see the bright side, often overthinking the worst possibilities.",
        "You could be risk-averse, preferring the comfort of the familiar over stepping into unknown territory.",
        "Your negative outlook might sometimes create unnecessary stress or anxiety."
    ],
    "emotion_based": {
        "Sadness": [
            "You may be deeply empathetic and sensitive to others' emotional pain.",
            "Your sadness can sometimes weigh you down, affecting your ability to stay engaged with others.",
            "You feel the emotional weight of situations deeply, which can give you profound insights into others’ needs."
        ],
        "Joy": [
            "Your optimism and positive energy uplift those around you.",
            "You radiate joy, and your ability to remain cheerful in the face of challenges inspires others.",
            "You possess an infectious enthusiasm that motivates others to stay upbeat."
        ],
        "Fear": [
            "You tend to worry about potential dangers, which can sometimes hinder your decision-making.",
            "Your fear of failure sometimes causes you to hesitate, even when opportunities arise.",
            "You are cautious in uncertain situations, ensuring you’re well-prepared before taking action."
        ],
        "Anger": [
            "Your anger can give you the drive to take action but may sometimes cloud your judgment.",
            "You may struggle to control your frustration, especially in high-pressure situations.",
            "Your intense reactions to conflict may make it difficult for you to maintain calm under pressure."
        ]
    }
}

strengths_templates = {
    "FormQuality": {
        "Excellent": [
            "Your attention to detail ensures that everything is organized and structured.",
            "You have a methodical approach, excelling at structuring and organizing even the most complex tasks.",
            "You excel in ensuring that everything is well-aligned and executed with precision."
        ],
        "Average": [
            "You tend to look at the bigger picture, focusing on overarching goals rather than minute details.",
            "While you may not focus on the finer aspects, your strength lies in maintaining an overview."
        ]
    },
    "DevelopmentalQuality": {
        "Good": [
            "You demonstrate excellent emotional resilience, handling life's ups and downs with maturity.",
            "Your emotional intelligence is a key strength, helping you manage stress and face challenges with composure."
        ],
        "Average": [
            "While you handle stress well, you sometimes find it difficult to bounce back from emotionally taxing situations.",
            "Your emotional resilience is good, but there are moments when you struggle to maintain balance."
        ]
    }
}

weaknesses_templates = {
    "negative_sentiment": [
        "You may have a tendency toward pessimism, which could prevent you from seeing opportunities.",
        "Your negative thinking sometimes creates unnecessary stress and limits your perspective."
    ],
    "emotion_based": {
        "Fear": [
            "Fear often keeps you from taking risks, even when opportunities arise.",
            "Your hesitation can lead to missed chances, especially when you overthink potential risks."
        ],
        "Sadness": [
            "Sadness can occasionally cause you to withdraw from others, making it hard for you to engage emotionally.",
            "Your tendency to focus on your own sadness can make it difficult to see the positive side of things."
        ]
    }
}

approach_templates = {
    "positive_sentiment": [
        "You tackle challenges with optimism and creativity, embracing each situation with enthusiasm.",
        "Your positive attitude allows you to remain calm and collected, even in high-pressure situations.",
        "You approach every challenge with excitement and determination, confident that you can overcome it."
    ],
    "negative_sentiment": [
        "You approach challenges cautiously, often overthinking the potential outcomes before making decisions.",
        "Your tendency to focus on the risks involved can make it hard for you to move quickly, but it also ensures that you're well-prepared."
    ],
    "neutral_sentiment": [
        "You approach challenges with a calm and level-headed mindset, weighing all options before taking action.",
        "You are neither overly optimistic nor pessimistic; instead, you approach problems pragmatically and systematically."
    ]
}
