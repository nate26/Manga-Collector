import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter, withInMemoryScrolling } from '@angular/router';

import { routes } from './app.routes';
import {
    provideHttpClient,
    withFetch,
    withInterceptors,
} from '@angular/common/http';
import { provideAnimations } from '@angular/platform-browser/animations';
import {
    ApolloClientOptions,
    ApolloLink,
    InMemoryCache,
} from '@apollo/client/core';
import { removeTypenameFromVariables } from '@apollo/client/link/remove-typename';
import { APOLLO_OPTIONS, Apollo } from 'apollo-angular';
import { HttpLink } from 'apollo-angular/http';
import { authInterceptor } from './services/interceptors/auth-interceptor';

export const REST_SERVER_URL = 'http://localhost:8050';
export const GQL_SERVER_URL = 'http://localhost:4001/graphql';

export const appConfig: ApplicationConfig = {
    providers: [
        provideHttpClient(withFetch(), withInterceptors([authInterceptor])),
        provideZoneChangeDetection({ eventCoalescing: true }),
        provideRouter(routes, withInMemoryScrolling({
            scrollPositionRestoration: 'top',
            anchorScrolling: 'enabled',
        })),
        provideAnimations(),
        {
            provide: APOLLO_OPTIONS,
            useFactory: (httpLink: HttpLink): ApolloClientOptions<unknown> => ({
                link: ApolloLink.from([
                    removeTypenameFromVariables(),
                    httpLink.create({ uri: GQL_SERVER_URL }),
                ]),
                cache: new InMemoryCache(),
            }),
            deps: [HttpLink],
        },
        Apollo,
    ],
};
