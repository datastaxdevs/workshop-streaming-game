package com.example.api;

import org.apache.pulsar.client.api.Producer;
import org.apache.pulsar.client.api.PulsarClientException;
import org.eclipse.microprofile.config.inject.ConfigProperty;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.annotation.PostConstruct;
import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;
import javax.websocket.OnClose;
import javax.websocket.OnMessage;
import javax.websocket.Session;
import javax.websocket.server.PathParam;
import javax.websocket.server.ServerEndpoint;
import java.nio.charset.StandardCharsets;

import static com.example.api.Messaging.makeGoodbyeUpdate;
import static com.example.api.Messaging.validatePosition;

@ServerEndpoint("/ws/player/{id}")
@ApplicationScoped
public class PlayerRoute {

    private final Logger log = LoggerFactory.getLogger(this.getClass());

    @ConfigProperty(name = "astra.streaming.producer-topic")
    String producerTopic;

    @Inject
    PulsarService pulsar;
    private Producer<byte[]> producer;

    @PostConstruct
    private void initialize() throws PulsarClientException {
        this.producer = pulsar.getClient()
                .newProducer()
                .topic(producerTopic)
                .create();
    }

    @OnMessage
    public void onMessage(String message, @PathParam("id") String id) throws PulsarClientException {
        try {
            JSONObject json = new JSONObject(message);
            // The other type is : "chat"
            if (json.has("messageType") && "player".equals(json.getString("messageType"))) {
                JSONObject jsonPayload = json.getJSONObject("payload");
                validatePosition(jsonPayload);
            }
            json.put("playerID", id);
            // Send to pulsar
            producer.send(json.toString().getBytes(StandardCharsets.UTF_8));
        } catch (Exception e) {
            String json = makeGoodbyeUpdate(id);
            producer.send(json.getBytes(StandardCharsets.UTF_8));
        }
    }

    @OnClose
    public void onClose(Session session, @PathParam("id") String id) throws PulsarClientException {
        log.info("Connection closed with User with id={}", id);
        String json = makeGoodbyeUpdate(id);
        producer.send(json.getBytes(StandardCharsets.UTF_8));
    }

}
