package com.example.api.websocket;

import lombok.extern.slf4j.Slf4j;
import org.apache.pulsar.client.api.Producer;
import org.apache.pulsar.client.api.PulsarClient;
import org.apache.pulsar.client.api.PulsarClientException;
import org.json.JSONObject;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;

import javax.annotation.PostConstruct;
import java.nio.charset.StandardCharsets;

import static com.example.api.util.Messaging.makeGoodbyeUpdate;
import static com.example.api.util.Messaging.validatePosition;

@Slf4j
@Component("PlayerRouteHandler")
public class PlayerRouteHandler extends TextWebSocketHandler {

    @Value("${astra.streaming.producer-topic}")
    private String producerTopic;

    private final PulsarClient pulsarClient;
    private Producer<byte[]> producer;

    public PlayerRouteHandler(PulsarClient pulsarClient) {
        this.pulsarClient = pulsarClient;
    }

    @PostConstruct
    private void initialize() throws PulsarClientException {
        this.producer = pulsarClient.newProducer()
                .topic(producerTopic)
                .create();
    }

    @Override
    protected void handleTextMessage(WebSocketSession session, TextMessage message) throws Exception {

        String payload = message.getPayload();

        try {
            JSONObject json = new JSONObject(payload);
            // The other type is : "chat"
            if (json.has("messageType") && "player".equals(json.getString("messageType"))) {
                JSONObject jsonPayload = json.getJSONObject("payload");
                validatePosition(jsonPayload);
            }
            json.put("playerID", session.getAttributes().get("id"));
            // Send to pulsar
            producer.send(json.toString().getBytes(StandardCharsets.UTF_8));
        } catch (Exception e) {
            String id = session.getAttributes().get("id").toString();
            String json = makeGoodbyeUpdate(id);
            producer.send(json.getBytes(StandardCharsets.UTF_8));
        }
    }

    @Override
    public void afterConnectionEstablished(WebSocketSession session) {
        String id = session.getAttributes().get("id").toString();
        log.info("Connection established with User with id={}", id);
    }

    @Override
    public void afterConnectionClosed(WebSocketSession session, CloseStatus status) throws PulsarClientException {
        String id = session.getAttributes().get("id").toString();
        log.info("Connection closed with User with id={}", id);

        String json = makeGoodbyeUpdate(id);
        producer.send(json.getBytes(StandardCharsets.UTF_8));
    }
}
