import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { provideHttpClient, withFetch } from '@angular/common/http';
import { provideAnimations } from '@angular/platform-browser/animations';
import { ApolloClientOptions, ApolloLink, InMemoryCache } from '@apollo/client/core';
import { APOLLO_OPTIONS, Apollo } from 'apollo-angular';
import { HttpLink } from 'apollo-angular/http';

export const appConfig: ApplicationConfig = {
    providers: [
        provideHttpClient(withFetch()),
        provideZoneChangeDetection({ eventCoalescing: true }),
        provideRouter(routes),
        provideAnimations(),
        {
            provide: APOLLO_OPTIONS,
            useFactory: (httpLink: HttpLink): ApolloClientOptions<unknown> => ({
                link: ApolloLink.from([
                    httpLink.create({ uri: 'http://localhost:4000/graphql' }),
                ]),
                cache: new InMemoryCache(),
            }),
            deps: [HttpLink],
        },
        Apollo,
    ]
};
