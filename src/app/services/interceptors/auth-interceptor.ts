import { HttpClient, HttpHandlerFn, HttpRequest } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthenticationData, UserData, UserService } from '../data/user.service';
import { switchMap, of, iif, map } from 'rxjs';
import { GQL_SERVER_URL, REST_SERVER_URL } from '../../app.config';

export function authInterceptor(req: HttpRequest<unknown>, next: HttpHandlerFn) {
    if (!req.url.startsWith(GQL_SERVER_URL)) {
        return next(req);
    }

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
        inject(HttpClient).post<AuthenticationData>(
            REST_SERVER_URL + '/refreshToken',
            { username, refresh_token }
        ).pipe(
            map(authentication => ({ ...userService.userData(), authentication } as UserData)),
            userService.saveUserData,
            map(({ authentication }) => authentication.token)
        )
    ).pipe(
        switchMap(providedToken => next(req.clone({
            headers: req.headers.append('X-Authentication-Token', providedToken!)
        })))
    );
}
