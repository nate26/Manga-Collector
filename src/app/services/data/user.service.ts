import { HttpClient } from '@angular/common/http';
import { Injectable, computed, inject, signal } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { ActivatedRoute } from '@angular/router';
import { Observable, pipe, shareReplay, switchMap, tap, throwError } from 'rxjs';
import { REST_SERVER_URL } from '../../app.config';

export type AuthenticationData = {
    token: string;
    expiration: string;
    refresh_token: string;
};

export type UserData = {
    username: string;
    email: string;
    user_id: string;
    profile: {
        picture: string | null;
        banner: string | null;
        color: string | null;
        theme: string | null;
    };
    personal_stores: string[];
    authentication: AuthenticationData;
}

export const LOGIN_PATH_CONTEXT = {
    path: '/login',
    name: 'Login'
};

export const SIGNUP_PATH_CONTEXT = {
    path: '/sign-up',
    name: 'Sign Up'
};

@Injectable({
    providedIn: 'root'
})
export class UserService {

    private readonly http = inject(HttpClient);
    private readonly _activatedRoute = inject(ActivatedRoute);

    userData = signal<UserData>({
        username: localStorage.getItem('username')!,
        email: localStorage.getItem('email')!,
        user_id: localStorage.getItem('user_id')!,
        profile: {
            picture: localStorage.getItem('picture'),
            banner: localStorage.getItem('banner'),
            color: localStorage.getItem('color'),
            theme: localStorage.getItem('theme')
        },
        personal_stores: JSON.parse(localStorage.getItem('personal_stores') ?? '[]'),
        authentication: {
            token: localStorage.getItem('token')!,
            expiration: localStorage.getItem('expiration')!,
            refresh_token: localStorage.getItem('refresh_token')!
        }
    });

    userDataIsValid = computed(() => {
        const userData = this.userData();
        return Boolean(
            userData.authentication.token &&
            userData.authentication.expiration &&
            userData.authentication.refresh_token &&
            userData.username &&
            userData.email &&
            userData.user_id
            //TODO add other validations once defaults get set
        )
    });

    userIdFromRoute$ = this._activatedRoute.queryParams.pipe(
        switchMap(params => {
            if (!params['username']) {
                return throwError(() => Error('No username provided.'));
            }
            return this.http.get<UserData>(
                REST_SERVER_URL + '/get-user-by-username?username=' + params['username']
            );
        }),
        shareReplay(1)
    );

    private readonly _routeChanged = toSignal(
        this._activatedRoute.queryParams,
        { initialValue: { username: null } }
    )
    canUserEdit = computed(() => this.userData().username === this._routeChanged().username);

    readonly saveUserData = pipe(
        tap((data: UserData) => {
            localStorage.setItem('token', data.authentication.token);
            localStorage.setItem('expiration', data.authentication.expiration);
            localStorage.setItem('refresh_token', data.authentication.refresh_token);
            localStorage.setItem('username', data.username);
            localStorage.setItem('email', data.email);
            localStorage.setItem('user_id', data.user_id);
            localStorage.setItem('picture', data.profile.picture ?? '');
            localStorage.setItem('banner', data.profile.banner ?? '');
            localStorage.setItem('color', data.profile.color ?? '');
            localStorage.setItem('theme', data.profile.theme ?? '');
            localStorage.setItem('personal_stores', JSON.stringify(data.personal_stores));
            this.userData.set(data);
        })
    );

    /**
     * Login for a user to get a token.
     * @param email the email to use, if not provided, an error is thrown
     * @param password the password to use, if not provided, an error is thrown
     * @returns a cached observable of the user's token
     */
    login(
        email: string | null | undefined,
        password: string | null | undefined
    ): Observable<UserData> {
        if (!email || !password) {
            return throwError(() => Error('Email and password are required to login.'));
        }
        return this.http.post<UserData>(REST_SERVER_URL + LOGIN_PATH_CONTEXT.path, { email, password }).pipe(
            this.saveUserData
        );
    }

    /**
     * Sign Up for a user to create an account and get a token.
     * @param email the email to use, if not provided, an error is thrown
     * @param username the username to use, if not provided, an error is thrown
     * @param password the password to use, if not provided, an error is thrown
     * @returns a cached observable of the user's token
     */
    signUp(
        email: string | null | undefined,
        username: string | null | undefined,
        password: string | null | undefined
    ): Observable<UserData> {
        if (!email || !username || !password) {
            return throwError(() => Error('Email, username, and password are required to sign up for an account.'));
        }
        return this.http.post<UserData>(REST_SERVER_URL + SIGNUP_PATH_CONTEXT.path, { email, username, password }).pipe(
            this.saveUserData
        );
    }

    /**
     * Check if a username is available.
     * @param username the username to check
     * @returns an observable of whether the username is available
     */
    checkUsername(username: string): Observable<boolean> {
        return this.http.post<boolean>(REST_SERVER_URL + '/check-username', { username });
    }

    /**
     * Log out the user. This clears the user's data from local storage.
     */
    logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('expiration');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('username');
        localStorage.removeItem('email');
        localStorage.removeItem('user_id');
        localStorage.removeItem('picture');
        localStorage.removeItem('banner');
        localStorage.removeItem('color');
        localStorage.removeItem('theme');
        localStorage.removeItem('personal_stores');
        this.userData.set({
            username: '',
            email: '',
            user_id: '',
            profile: {
                picture: null,
                banner: null,
                color: null,
                theme: null
            },
            personal_stores: [],
            authentication: {
                token: '',
                expiration: '',
                refresh_token: ''
            }
        });
    }

}
