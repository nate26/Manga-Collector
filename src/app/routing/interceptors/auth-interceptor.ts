import { HttpHandlerFn, HttpRequest } from '@angular/common/http';
import { inject } from '@angular/core';
import { catchError, iif, map, of, switchMap, tap } from 'rxjs';
import { REST_SERVER_URL } from '../../app.config';
import { UserData } from '../../services/data/user.type';
import { UserService } from '../data/user.service';
import { LoginService } from '../login.service';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function authInterceptor(req: HttpRequest<any>, next: HttpHandlerFn) {
  if (!req.url.startsWith(REST_SERVER_URL) || req.body?.['operationName'] === 'refreshToken') {
    return next(req);
  }

  const loginService = inject(LoginService);
  const userService = inject(UserService);
  const { authentication } = userService.userData();

  const { token, refresh_token, expiration } = authentication;
  if (!token || !refresh_token || !expiration) {
    return next(req);
  }

  return iif(
    () => parseFloat(expiration!) > Date.now() / 1000 && Boolean(token),
    of(token),
    // inject(Apollo)
    //   .mutate<{ refresh_token: AuthenticationData }>({
    //     mutation: gql`
    //       mutation refreshToken($username: String!, $refresh_token: String!) {
    //         refresh_token(username: $username, refresh_token: $refresh_token) {
    //           token
    //           expiration
    //           refresh_token
    //         }
    //       }
    //     `,
    //     variables: { username, refresh_token }
    //   })
    of({ data: null, errors: Error('no login') } as any).pipe(
      tap(({ errors }) => {
        if (errors) throw errors;
      }),
      map(
        ({ data }) =>
          ({ ...userService.userData(), authentication: data!.refresh_token }) as UserData
      ),
      userService.saveUserData,
      map(({ authentication }) => authentication.token),
      catchError(() => {
        userService.logout();
        return loginService.openLogin().pipe(map(userData => userData?.authentication.token));
      })
    )
  ).pipe(
    switchMap(providedToken =>
      next(
        req.clone({
          headers: req.headers.append('X-Authentication-Token', providedToken!)
        })
      )
    )
  );
}
