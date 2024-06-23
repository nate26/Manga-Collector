import { HttpClient } from '@angular/common/http';
import { Injectable, computed, inject, signal } from '@angular/core';
import { toObservable } from '@angular/core/rxjs-interop';
import { Observable, filter, shareReplay, switchMap, tap } from 'rxjs';

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
    private readonly SERVER_URL = 'http://localhost:8050/';

    private _isLoggedIn = signal(false);
    /**
     * An observable of whether the user is logged in.
     */
    isLoggedIn = computed(() => this._isLoggedIn());

    private readonly _loginData = signal({ username: '', password: '', path: '' });

    /**
     * An observable of the user's auth token. This observable is cached and shared among subscribers.
     */
    userData$ = toObservable(this._loginData).pipe(
        filter(({ username, password }) => Boolean(username && password)),
        switchMap(({ username, password, path }) =>
            this.http.post<UserData>(this.SERVER_URL + path, { username, password })),
        tap(data => {
            window.localStorage.setItem('token', data.authentication.token);
            window.localStorage.setItem('expiration', data.authentication.expiration);
            window.localStorage.setItem('refresh_token', data.authentication.refresh_token);
            this._isLoggedIn.set(true)
        }),
        shareReplay()
    );

    /**
     * Login or Sign Up for a user to get a token.
     * @param username the user's entered username
     * @param password the user's entered password
     * @param path the path to login or sign up
     * @returns a cached observable of the user's token
     */
    login(username: string, password: string, path: string): Observable<UserData> {
        this._loginData.set({ username, password, path });
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
     * Log out the user.
     */
    signOut() {
        window.localStorage.removeItem('token');
        window.localStorage.removeItem('expiration');
        window.localStorage.removeItem('refresh_token');
        this._isLoggedIn.set(false);
        this._loginData.set({ username: '', password: '', path: '' });
    }

}
