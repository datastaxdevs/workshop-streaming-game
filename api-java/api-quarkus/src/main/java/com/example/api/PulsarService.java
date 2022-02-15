package com.example.api;

import org.apache.pulsar.client.api.AuthenticationFactory;
import org.apache.pulsar.client.api.PulsarClient;
import org.apache.pulsar.client.api.PulsarClientException;
import org.eclipse.microprofile.config.inject.ConfigProperty;

import javax.enterprise.context.ApplicationScoped;


@ApplicationScoped
public class PulsarService {

    private final PulsarClient pulsarClient;

    public PulsarService(@ConfigProperty(name = "astra.service.url") String serviceUrl,
                         @ConfigProperty(name = "astra.auth.token") String authToken) throws PulsarClientException {
        this.pulsarClient = PulsarClient.builder()
                .serviceUrl(serviceUrl)
                .authentication(AuthenticationFactory.token(authToken))
                .build();
    }

    public PulsarClient getClient() {
        return pulsarClient;
    }

}
