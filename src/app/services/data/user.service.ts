import { HttpClient } from '@angular/common/http';
import { Injectable, inject, signal } from '@angular/core';
import { toObservable, toSignal } from '@angular/core/rxjs-interop';
import { Router } from '@angular/router';
import { Observable, filter, iif, map, of, shareReplay, switchMap, tap } from 'rxjs';

export type UserData = {
    username: string;
    user_id: string;
    profile: {
        picture: string | null;
        banner: string | null;
        color: string | null;
        theme: string | null;
    };
    personal_stores: string[];
    authentication: {
        token: string;
        expiration: string;
        refresh_token: string;
    };
}

@Injectable({
    providedIn: 'root'
})
export class UserService {

    private readonly http = inject(HttpClient);
    private readonly router = inject(Router);
    private readonly SERVER_URL = 'http://localhost:8050/';

    private readonly _loginData = signal({ username: '', password: '', loginOrSignInPath: '' });

    private readonly _userData$ = toObservable(this._loginData).pipe(
        switchMap(({ username, password, loginOrSignInPath }) => {
            const cachedToken = localStorage.getItem('token');
            const cachedExpiration = localStorage.getItem('expiration');
            const cachedRefreshToken = localStorage.getItem('refresh_token');
            const cachedUsername = localStorage.getItem('username');
            const cachedUserId = localStorage.getItem('user_id');
            return iif(
                () => Boolean(cachedToken && cachedExpiration && cachedRefreshToken && cachedUsername && cachedUserId),
                of(<UserData>{
                    username: cachedUsername,
                    user_id: cachedUserId,
                    profile: {
                        picture: localStorage.getItem('picture'),
                        banner: localStorage.getItem('banner'),
                        color: localStorage.getItem('color'),
                        theme: localStorage.getItem('theme')
                    },
                    personal_stores: JSON.parse(localStorage.getItem('personal_stores') ?? '[]'),
                    authentication: {
                        token: cachedToken,
                        expiration: cachedExpiration,
                        refresh_token: cachedRefreshToken
                    }
                }),
                iif(
                    () => Boolean(username && password && loginOrSignInPath),
                    this.http.post<UserData>(this.SERVER_URL + loginOrSignInPath, { username, password }).pipe(
                        tap(data => {
                            localStorage.setItem('token', data.authentication.token);
                            localStorage.setItem('expiration', data.authentication.expiration);
                            localStorage.setItem('refresh_token', data.authentication.refresh_token);
                            localStorage.setItem('username', data.username);
                            localStorage.setItem('user_id', data.user_id);
                            localStorage.setItem('picture', data.profile.picture ?? '');
                            localStorage.setItem('banner', data.profile.banner ?? '');
                            localStorage.setItem('color', data.profile.color ?? '');
                            localStorage.setItem('theme', data.profile.theme ?? '');
                            localStorage.setItem('personal_stores', JSON.stringify(data.personal_stores));
                        })
                    ),
                    of(null)
                )
            );
        }),
        shareReplay()
    );

    /**
     * An observable of the user's auth token. This observable is cached and shared among subscribers.
     * If the user is not logged in, this observable will emit null.
     */
    // ugh typescript stuff... this is a hack to get the type to be correct
    userData$ = <Observable<UserData>>this._userData$.pipe(filter(data => Boolean(data)));

    /**
     * An signal of whether the user is logged in.
     */
    isLoggedIn = toSignal(this._userData$.pipe(map(data => Boolean(data))), { initialValue: false });

    /**
     * Login or Sign Up for a user to get a token.
     * @param username the user's entered username
     * @param password the user's entered password
     * @param path the path to login or sign up
     * @returns a cached observable of the user's token
     */
    login(username: string, password: string, loginOrSignInPath: string): Observable<UserData> {
        this._loginData.set({ username, password, loginOrSignInPath });
        return this.userData$;
    }

    /**
     * Check if a username is available.
     * @param username the username to check
     * @returns an observable of whether the username is available
     */
    checkUsername(username: string): Observable<boolean> {
        return this.http.post<boolean>(this.SERVER_URL + '/check-username', { username });
    }

    /**
     * Log out the user. This clears the user's data from local storage.
     */
    logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('expiration');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('username');
        localStorage.removeItem('user_id');
        localStorage.removeItem('picture');
        localStorage.removeItem('banner');
        localStorage.removeItem('color');
        localStorage.removeItem('theme');
        localStorage.removeItem('personal_stores');
        this._loginData.set({ username: '', password: '', loginOrSignInPath: '' });
        this.router.navigateByUrl('/login');
    }

}
