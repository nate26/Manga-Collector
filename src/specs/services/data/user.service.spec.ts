import { TestBed } from '@angular/core/testing';
import { UserData, UserService } from '../../../app/services/data/user.service';
import { HttpClient } from '@angular/common/http';
import { ActivatedRoute, Params } from '@angular/router';
import { catchError, forkJoin, of, Subject } from 'rxjs';

describe('UserService', () => {
    let service: UserService;
    let httpMock: jasmine.SpyObj<HttpClient>;
    let activatedRouteMock: jasmine.SpyObj<ActivatedRoute>;
    let routeSub: Subject<Params>;

    const MOCK_USER_DATA = {
        username: 'test',
        email: 'test@gmail.com',
        user_id: '1',
        profile: {
            picture: 'picture',
            banner: 'banner',
            color: 'color',
            theme: 'theme'
        },
        personal_stores: ['store'],
        authentication: {
            token: 'token',
            expiration: 'expiration',
            refresh_token: 'refresh_token'
        }
    };

    beforeEach(() => {
        httpMock = jasmine.createSpyObj(['get', 'post']);
        routeSub = new Subject<Params>();
        activatedRouteMock = {
            ...jasmine.createSpyObj([], ['queryParams']),
            queryParams: routeSub.asObservable()
        };
    });

    describe('User Data', () => {

        beforeEach(() => {
            TestBed.configureTestingModule({
                providers: [
                    { provide: HttpClient, useValue: httpMock },
                    { provide: ActivatedRoute, useValue: activatedRouteMock }
                ]
            });
            window.localStorage.clear();
            service = TestBed.inject(UserService);
        });

        it('should validate that user data is valid', () => {
            service.userData.set(MOCK_USER_DATA);
            const isValid = service.userDataIsValid();
            expect(isValid).toBeTrue();
        });

        it('should validate that user data is not valid', () => {
            expect(service.userDataIsValid()).toBeFalse();

            const invalidAuthKeys = ['token', 'expiration', 'refresh_token'];
            invalidAuthKeys.forEach(key => {
                service.userData.set({
                    ...MOCK_USER_DATA,
                    authentication: {
                        ...MOCK_USER_DATA.authentication,
                        [key]: null
                    }
                });
                expect(service.userDataIsValid()).toBeFalse();
            });

            const invalidKeys = ['username', 'email', 'user_id'];
            invalidKeys.forEach(key => {
                service.userData.set({
                    ...MOCK_USER_DATA,
                    [key]: null
                });
                expect(service.userDataIsValid()).toBeFalse();
            });
        });

        it('should get user data from route id', (done) => {
            httpMock.get.and.returnValue(of(MOCK_USER_DATA));
            service.userIdFromRoute$.subscribe({
                next: data => {
                    expect(data).toEqual(MOCK_USER_DATA);
                    done();
                },
                error: done.fail
            });
            routeSub.next({ username: 'test' });
            expect(httpMock.get).toHaveBeenCalledOnceWith(
                'http://localhost:8050/get-user-by-username?username=test'
            );
        });

        it('should fail to get user data from route id if there is no username', () => {
            service.userIdFromRoute$.subscribe({
                next: () => fail('Should not have returned data.'),
                error: fail
            });
            routeSub.next({});
            expect(httpMock.get).not.toHaveBeenCalled();
        });

        it('should validate that user can edit', () => {
            httpMock.get.and.returnValue(of({ ...MOCK_USER_DATA, user_id: '123' }));
            service.userData.set({ ...MOCK_USER_DATA, user_id: '123' });
            routeSub.next({ username: 'test' });
            expect(service.canUserEdit()).toBeTrue();
        });

        it('should validate that user cannot edit on default without a route', () => {
            service.userData.set(MOCK_USER_DATA);
            expect(service.canUserEdit()).toBeFalse();
        });

        it('should validate that user cannot edit when username does not match', () => {
            httpMock.get.and.returnValue(of({ ...MOCK_USER_DATA, user_id: '123' }));
            service.userData.set({ ...MOCK_USER_DATA, user_id: '789' });
            routeSub.next({ username: 'test' });
            expect(service.canUserEdit()).toBeFalse();
        });

        it('should check username', (done) => {
            httpMock.post.and.returnValues(of(true), of(false));
            forkJoin([
                service.checkUsername('test1'),
                service.checkUsername('test2')
            ]).subscribe({
                next: data => {
                    expect(data).toEqual([true, false]);
                    expect(httpMock.post).toHaveBeenCalledTimes(2);
                    expect(httpMock.post.calls.first().args).toEqual([
                        'http://localhost:8050/check-username',
                        { username: 'test1' }
                    ]);
                    expect(httpMock.post.calls.mostRecent().args).toEqual([
                        'http://localhost:8050/check-username',
                        { username: 'test2' }
                    ]);
                    done();
                },
                error: fail
            });
        });
    });

    describe('Local Storage', () => {

        beforeEach(() => {
            localStorage.setItem('username', 'user');
            localStorage.setItem('email', 'user@gmail.com');
            localStorage.setItem('user_id', '123');
            localStorage.setItem('picture', 'my picture');
            localStorage.setItem('banner', 'my banner');
            localStorage.setItem('color', 'my color');
            localStorage.setItem('theme', 'my theme');
            localStorage.setItem('personal_stores', '["my store"]');
            localStorage.setItem('token', '111');
            localStorage.setItem('expiration', '222');
            localStorage.setItem('refresh_token', '333');
            TestBed.configureTestingModule({
                providers: [
                    { provide: HttpClient, useValue: httpMock },
                    { provide: ActivatedRoute, useValue: activatedRouteMock }
                ]
            });
            service = TestBed.inject(UserService);
        });

        it('should get user data from local storage', () => {
            expect(service.userData()).toEqual({
                username: 'user',
                email: 'user@gmail.com',
                user_id: '123',
                profile: {
                    picture: 'my picture',
                    banner: 'my banner',
                    color: 'my color',
                    theme: 'my theme'
                },
                personal_stores: ['my store'],
                authentication: {
                    token: '111',
                    expiration: '222',
                    refresh_token: '333'
                }
            });
        });

        it('should save user data to local storage', () => {
            of(MOCK_USER_DATA).pipe(service.saveUserData).subscribe();
            expect(localStorage.getItem('username')).toBe('test');
            expect(localStorage.getItem('email')).toBe('test@gmail.com');
            expect(localStorage.getItem('user_id')).toBe('1');
            expect(localStorage.getItem('picture')).toBe('picture');
            expect(localStorage.getItem('banner')).toBe('banner');
            expect(localStorage.getItem('color')).toBe('color');
            expect(localStorage.getItem('theme')).toBe('theme');
            expect(localStorage.getItem('personal_stores')).toBe('["store"]');
            expect(localStorage.getItem('token')).toBe('token');
            expect(localStorage.getItem('expiration')).toBe('expiration');
            expect(localStorage.getItem('refresh_token')).toBe('refresh_token');
        });

        it('should save user data to local storage with nulls', () => {
            of({
                ...MOCK_USER_DATA,
                profile: {
                    picture: null,
                    banner: null,
                    color: null,
                    theme: null
                },
                personal_stores: []
            }).pipe(service.saveUserData).subscribe();
            expect(localStorage.getItem('picture')).toBe('');
            expect(localStorage.getItem('banner')).toBe('');
            expect(localStorage.getItem('color')).toBe('');
            expect(localStorage.getItem('theme')).toBe('');
            expect(localStorage.getItem('personal_stores')).toBe('[]');
        });

        it('should login with email and password and save to local storage', () => {
            httpMock.post.and.returnValue(of(MOCK_USER_DATA));
            let userData: UserData;
            service.login('user@gmail.com', 'password').subscribe({
                next: data => userData = data,
                error: fail
            });
            expect(userData!).toEqual(MOCK_USER_DATA);
            expect(httpMock.post).toHaveBeenCalledOnceWith(
                'http://localhost:8050/login',
                { email: 'user@gmail.com', password: 'password' }
            );
            expect(localStorage.getItem('username')).toBe('test');
            expect(localStorage.getItem('email')).toBe('test@gmail.com');
            expect(localStorage.getItem('user_id')).toBe('1');
            expect(localStorage.getItem('picture')).toBe('picture');
            expect(localStorage.getItem('banner')).toBe('banner');
            expect(localStorage.getItem('color')).toBe('color');
            expect(localStorage.getItem('theme')).toBe('theme');
            expect(localStorage.getItem('personal_stores')).toBe('["store"]');
            expect(localStorage.getItem('token')).toBe('token');
            expect(localStorage.getItem('expiration')).toBe('expiration');
            expect(localStorage.getItem('refresh_token')).toBe('refresh_token');
        });

        it('should fail to login without email or password', (done) => {
            forkJoin(
                [
                    service.login('user@gmail.com', null),
                    service.login('user@gmail.com', undefined),
                    service.login(null, 'password'),
                    service.login(undefined, 'password')
                ].map(obs => obs.pipe(
                    catchError((err: Error) => of(err.message))
                ))
            ).subscribe({
                next: data => {
                    expect(data)
                        .toEqual(Array(4).fill('Email and password are required to login.'));
                    done();
                },
                error: fail
            });
        });

        it('should signup with email, username, and password and save to local storage', () => {
            httpMock.post.and.returnValue(of(MOCK_USER_DATA));
            let userData: UserData;
            service.signUp('user@gmail.com', 'user', 'password').subscribe({
                next: data => userData = data,
                error: fail
            });
            expect(userData!).toEqual(MOCK_USER_DATA);
            expect(httpMock.post).toHaveBeenCalledOnceWith(
                'http://localhost:8050/sign-up',
                { email: 'user@gmail.com', username: 'user', password: 'password' }
            );
            expect(localStorage.getItem('username')).toBe('test');
            expect(localStorage.getItem('email')).toBe('test@gmail.com');
            expect(localStorage.getItem('user_id')).toBe('1');
            expect(localStorage.getItem('picture')).toBe('picture');
            expect(localStorage.getItem('banner')).toBe('banner');
            expect(localStorage.getItem('color')).toBe('color');
            expect(localStorage.getItem('theme')).toBe('theme');
            expect(localStorage.getItem('personal_stores')).toBe('["store"]');
            expect(localStorage.getItem('token')).toBe('token');
            expect(localStorage.getItem('expiration')).toBe('expiration');
            expect(localStorage.getItem('refresh_token')).toBe('refresh_token');
        });

        it('should fail to signup without email, username, or password', (done) => {
            forkJoin(
                [
                    service.signUp('user@gmail.com', 'name', null),
                    service.signUp('user@gmail.com', 'name', undefined),
                    service.signUp(null, 'name', 'password'),
                    service.signUp(undefined, 'name', 'password'),
                    service.signUp('user@gmail.com', null, 'password'),
                    service.signUp('user@gmail.com', null, 'password')
                ].map(obs => obs.pipe(
                    catchError((err: Error) => of(err.message))
                ))
            ).subscribe({
                next: data => {
                    expect(data).toEqual(Array(6).fill(
                        'Email, username, and password are required to sign up for an account.'
                    ));
                    done();
                },
                error: fail
            });
        });

        it('should get user data from local storage', () => {
            service.userData.set(MOCK_USER_DATA);
            service.logout();
            expect(localStorage.getItem('username')).toBeNull();
            expect(localStorage.getItem('email')).toBeNull();
            expect(localStorage.getItem('user_id')).toBeNull();
            expect(localStorage.getItem('picture')).toBeNull();
            expect(localStorage.getItem('banner')).toBeNull();
            expect(localStorage.getItem('color')).toBeNull();
            expect(localStorage.getItem('theme')).toBeNull();
            expect(localStorage.getItem('personal_stores')).toBeNull();
            expect(localStorage.getItem('token')).toBeNull();
            expect(localStorage.getItem('expiration')).toBeNull();
            expect(localStorage.getItem('refresh_token')).toBeNull();
            expect(service.userData()).toEqual({
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
        });

    });
});
