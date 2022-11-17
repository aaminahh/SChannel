{
    "rules": {
        "SChannel": {
            "Channels" : {
                ".indexOn": ["First Name", "Last Name", "Email", "Phone Number", "User ID", "Channel Group ID"]
            },
            ".read": true,
            ".write": true
        }
    }
}
{
    "rules": {
        "SChannel": {
            "ChannelGroups" : {
                ".indexOn": ["age", "gender", "occupation", "zipCode"]
            },
            ".read": true,
            ".write": true
        }
    }
}
{
    "rules": {
        "SChannel": {
            "Worfklows" : {
                ".indexOn": ["age", "gender", "occupation", "zipCode"]
            },
            ".read": true,
            ".write": true
        }
    }
}