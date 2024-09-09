import { HttpHandlerFn, HttpRequest } from '@angular/common/http';
import { inject } from '@angular/core';
import { switchMap, of, iif, map, tap, catchError } from 'rxjs';
import { GQL_SERVER_URL } from '../../app.config';
import { UserService } from '../data/user.service';
import { AuthenticationData, UserData } from '../../interfaces/iUserData.type';
import { Apollo, gql } from 'apollo-angular';
import { LoginService } from '../login.service';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function authInterceptor(req: HttpRequest<any>, next: HttpHandlerFn) {
    if (!req.url.startsWith(GQL_SERVER_URL) || req.body?.['operationName'] === 'refreshToken') {
        return next(req);
    }

    const loginService = inject(LoginService);
    const userService = inject(UserService);
    const { username, authentication } = userService.userData();

    const { token, refresh_token, expiration } = authentication;
    if (!token || !refresh_token || !expiration) {
        return next(req);
    }

    return iif(
        () => parseFloat(expiration!) > (Date.now() / 1000)
            && Boolean(token),
        of(token),
        inject(Apollo).mutate<{ refresh_token: AuthenticationData }>({
            mutation: gql`
                mutation refreshToken($username: String!, $refresh_token: String!) {
                    refresh_token(username: $username, refresh_token: $refresh_token) {
                        token
                        expiration
                        refresh_token
                    }
                }
            `,
            variables: { username, refresh_token }
        }).pipe(
            tap(({ errors }) => {
                if (errors) throw errors;
            }),
            map(({ data }) => ({ ...userService.userData(), authentication: data!.refresh_token } as UserData)),
            userService.saveUserData,
            map(({ authentication }) => authentication.token),
            catchError(() => {
                userService.logout();
                return loginService.openLogin().pipe(
                    map(userData => userData?.authentication.token)
                );
            })
        )
    ).pipe(
        switchMap(providedToken => next(req.clone({
            headers: req.headers.append('X-Authentication-Token', providedToken!)
        })))
    );
}
