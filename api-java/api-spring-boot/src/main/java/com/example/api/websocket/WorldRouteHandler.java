package com.example.api.websocket;

import lombok.extern.slf4j.Slf4j;
import org.apache.pulsar.client.api.Consumer;
import org.apache.pulsar.client.api.MessageListener;
import org.apache.pulsar.client.api.PulsarClient;
import org.apache.pulsar.client.api.PulsarClientException;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;

import javax.annotation.PostConstruct;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

import static com.example.api.util.Messaging.makeGeometryUpdate;


@Slf4j
@Component("WorldRouteHandler")
public class WorldRouteHandler extends TextWebSocketHandler {

    @Value("${astra.streaming.consumer-topic}")
    private String topic;

    private final Map<String, WebSocketSession> worldSessions = new ConcurrentHashMap<>();
    private final PulsarClient pulsarClient;
    private Consumer<byte[]> consumer;

    public WorldRouteHandler(PulsarClient pulsarClient) {
        this.pulsarClient = pulsarClient;
    }

    @PostConstruct
    private void initialize() throws PulsarClientException {
        MessageListener<byte[]> myMessageListener = (consumer, msg) -> {
            try {
                String received =  new String(msg.getData());
                for (Map.Entry<String, WebSocketSession> entry : worldSessions.entrySet()) {
                    WebSocketSession v = entry.getValue();
                    v.sendMessage(new TextMessage(received));
                }
                consumer.acknowledge(msg);
            } catch (Exception e) {
                consumer.negativeAcknowledge(msg);
            }
        };

        this.consumer = pulsarClient.newConsumer()
                .topic(topic)
                .subscriptionName("game-subscription")
                .messageListener(myMessageListener)
                .subscribe();
    }

    @Override
    protected void handleTextMessage(WebSocketSession session, TextMessage message) throws Exception {
        log.info("Handle Text message in the World Route... Zzzzz...");
    }

    @Override
    public void afterConnectionEstablished(WebSocketSession session) throws Exception {
        String id = (String) session.getAttributes().get("id");
        log.info("Connection established with User with id={}", id);
        worldSessions.put(id, session);

        // Note: this message is built here (i.e. no Pulsar involved)
        // and directly sent to a single client, the one who just connected:
        String position = makeGeometryUpdate();
        session.sendMessage(new TextMessage(position));
    }

    @Override
    public void afterConnectionClosed(WebSocketSession session, CloseStatus status) throws Exception {
        String id = (String) session.getAttributes().get("id");
        log.info("Connection closed with User with id={}", id);
        worldSessions.remove(id);
    }
}
