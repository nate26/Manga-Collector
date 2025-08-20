import { Injectable, computed, inject, signal } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { ActivatedRoute } from '@angular/router';
import { catchError, EMPTY, filter, map, Observable, pipe, shareReplay, switchMap, tap, throwError } from 'rxjs';
import { Apollo, gql } from 'apollo-angular';
import { UserDataPartial, UserData } from '../../interfaces/iUserData.type';

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

    private readonly _apollo = inject(Apollo);
    private readonly _activatedRoute = inject(ActivatedRoute);

    readonly userData = signal<UserDataPartial>({
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

    readonly userDataIsValid = computed(() => {
        const userData = this.userData();
        return Boolean(
            userData.authentication.token &&
            userData.authentication.expiration &&
            userData.authentication.refresh_token &&
            userData.username &&
            userData.email &&
            userData.user_id
            //TODO add other validations once defaults get set
        );
    });

    readonly userIdFromRoute$ = this._activatedRoute.queryParams.pipe(
        filter(params => Boolean(params['username'])),
        switchMap(params => this._apollo.query<{ get_user: { user_id: string } }>({
            query: gql`
                query get_user($username: String!) {
                    get_user(username: $username) {
                        user_id
                    }
                }
            `,
            variables: {
                username: params['username']
            }
        })),
        tap(({ error }) => {
            if (error) throw error;
        }),
        map(result => result.data.get_user.user_id),
        catchError((err: Error) => {
            console.error('Could not get user data because ', err);
            return EMPTY;
        }),
        shareReplay(1)
    );

    private readonly _userIdOnRoute = toSignal<string, string>(
        this.userIdFromRoute$,
        { initialValue: '' }
    );
    readonly canUserEdit = computed(() => this.userData().user_id === this._userIdOnRoute());

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
        return this._apollo.query<{ login: UserData }>({
            query: gql`
                query login($email: String!, $password: String!) {
                    login(email: $email, password: $password) {
                        email
                        username
                        user_id
                        profile {
                            picture
                            banner
                            color
                            theme
                        }
                        personal_stores
                        authentication {
                            token
                            expiration
                            refresh_token
                        }
                    }
                }
            `,
            variables: {
                email,
                password
            }
        }).pipe(
            tap(({ error }) => {
                if (error) throw error;
            }),
            map(result => result.data.login),
            this.saveUserData,
            catchError((err: Error) => {
                console.error('Could not login because ', err);
                return EMPTY;
            })
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
        return this._apollo.query<{ sign_up: UserData }>({
            query: gql`
                query sign_up($email: String!, $username: String!, $password: String!) {
                    sign_up(email: $email, username: $username, password: $password) {
                        email
                        username
                        user_id
                        profile {
                            picture
                            banner
                            color
                            theme
                        }
                        personal_stores
                        authentication {
                            token
                            expiration
                            refresh_token
                        }
                    }
                }
            `,
            variables: {
                email,
                username,
                password
            }
        }).pipe(
            tap(({ error }) => {
                if (error) throw error;
            }),
            map(result => result.data.sign_up),
            this.saveUserData,
            catchError((err: Error) => {
                console.error('Could not sign up because ', err);
                return EMPTY;
            })
        );
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
