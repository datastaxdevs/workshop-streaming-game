package com.example.api.config;

import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.socket.WebSocketHandler;
import org.springframework.web.socket.config.annotation.*;

@Configuration
@EnableWebSocket
public class WebsocketConfig implements WebSocketConfigurer {

    private final WebSocketHandler worldRouteHandler;
    private final WebSocketHandler playerRouteHandler;

    public WebsocketConfig(@Qualifier("WorldRouteHandler") WebSocketHandler worldRouteHandler,
                           @Qualifier("PlayerRouteHandler") WebSocketHandler playerRouteHandler) {
        this.worldRouteHandler = worldRouteHandler;
        this.playerRouteHandler = playerRouteHandler;
    }

    @Override
    public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {

        registry.addHandler(worldRouteHandler, "/ws/world/*")
                .setAllowedOrigins("*")
                .addInterceptors(new GameHandshakeInterceptor());

        registry.addHandler(playerRouteHandler, "/ws/player/*")
                .setAllowedOrigins("*")
                .addInterceptors(new GameHandshakeInterceptor());

    }
}
