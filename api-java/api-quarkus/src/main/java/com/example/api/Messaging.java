package com.example.api;

import org.json.JSONObject;

import java.util.UUID;

public class Messaging {

    private static final int HALF_SIZE_X = 20;
    private static final int HALF_SIZE_Y = 12;

    public static void validatePosition(JSONObject payload){
        if (!payload.isNull("x") && !payload.isNull("y")) {
            int x = sanitizePosition(payload.getInt("x"), HALF_SIZE_X);
            int y = sanitizePosition(payload.getInt("y"), HALF_SIZE_Y);
            payload.put("x", x);
            payload.put("y", y);
        }
    }

    private static int sanitizePosition(int val, int max) {
        if (val < 0) return 0;
        return Math.min(val, 2 * max - 2);
    }

    // A default goodbye message to publish to the Pulsar topic
    // in case a client disconnection is detected
    public static String makeGoodbyeUpdate(String clientId){
        return """
                {
                    "messageType":"player",
                    "playerID": "%s",
                    "payload":{
                        "x": null,
                        "y": null,
                        "h": false,
                        "generation": 0,
                        "playerName": ""
                    }
                }
                """.formatted(clientId);
    }

    // A server-generated chat message to greet a new player
    public static String makeWelcomeUpdate(){
        return """
                {
                    "messageType":"chat",
                    "playerID": "_api_server_",
                    "payload":{
                        "id": "%s",
                        "playerName": "** API **",
                        "text": "Welcome to the game!"
                    }
                }
                """.formatted(UUID.randomUUID().toString());
    }

    // Prepare a message containing the field geometry info
    public static String makeGeometryUpdate(){
        return """
                {
                    "messageType":"geometry",
                    "payload":{
                        "halfSizeX": %d,
                        "halfSizeY": %d
                    }
                }
                """.formatted(HALF_SIZE_X, HALF_SIZE_Y);
    }
}
