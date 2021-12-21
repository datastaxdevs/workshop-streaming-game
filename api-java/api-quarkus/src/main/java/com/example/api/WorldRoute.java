package com.example.api;

import org.apache.pulsar.client.api.Consumer;
import org.apache.pulsar.client.api.MessageListener;
import org.apache.pulsar.client.api.PulsarClientException;
import org.eclipse.microprofile.config.inject.ConfigProperty;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.annotation.PostConstruct;
import javax.enterprise.context.ApplicationScoped;
import javax.inject.Inject;
import javax.websocket.OnClose;
import javax.websocket.OnOpen;
import javax.websocket.Session;
import javax.websocket.server.PathParam;
import javax.websocket.server.ServerEndpoint;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

import static com.example.api.Messaging.makeGeometryUpdate;

@ServerEndpoint("/ws/world/{id}")
@ApplicationScoped
public class WorldRoute {

    @ConfigProperty(name = "astra.streaming.consumer-topic")
    String consumerTopic;
    @Inject
    PulsarService pulsar;

    private final Logger log = LoggerFactory.getLogger(this.getClass());
    private final Map<String, Session> worldSessions = new ConcurrentHashMap<>();
    private Consumer<byte[]> consumer;

    @PostConstruct
    private void initialize() throws PulsarClientException {
        MessageListener<byte[]> myMessageListener = (consumer, msg) -> {
            try {
                String received =  new String(msg.getData());
                broadcast(received);
                consumer.acknowledge(msg);
            } catch (Exception e) {
                consumer.negativeAcknowledge(msg);
            }
        };

        this.consumer = pulsar.getClient()
                .newConsumer()
                .topic(consumerTopic)
                .subscriptionName("game-subscription")
                .messageListener(myMessageListener)
                .subscribe();
    }

    @OnOpen
    public void onOpen(Session session, @PathParam("id") String id) {
        log.info("Connection established with User with id={}", id);
        worldSessions.put(id, session);

        String position = makeGeometryUpdate();
        session.getAsyncRemote().sendText(position);
    }

    @OnClose
    public void onClose(Session session, @PathParam("id") String id) {
        log.info("Connection closed with User with id={}", id);
        worldSessions.remove(id);
    }

    private void broadcast(String message) {
        worldSessions.values().forEach(s -> {
            s.getAsyncRemote().sendText(message, result ->  {
                if (result.getException() != null) {
                    log.error("Unable to send message: {}", result.getException().getMessage());
                }
            });
        });
    }
}
