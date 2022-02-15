package com.example.api.config;

import org.apache.pulsar.client.api.AuthenticationFactory;
import org.apache.pulsar.client.api.PulsarClient;
import org.apache.pulsar.client.api.PulsarClientException;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class PulsarConfig {

    @Bean
    public PulsarClient pulsarClient(@Value("${astra.service.url}") String serviceUrl,
                                     @Value("${astra.auth.token}") String authToken) throws PulsarClientException {

        return PulsarClient.builder()
                .serviceUrl(serviceUrl)
                .authentication(AuthenticationFactory.token(authToken))
                .build();
    }

}
