import { UserService } from '../../../app/services/data/user.service';
import { signal } from '@angular/core';
import { of, pipe, tap } from 'rxjs';
import { GQL_SERVER_URL, REST_SERVER_URL } from '../../../app/app.config';
import { authInterceptor } from '../../../app/services/interceptors/auth-interceptor';
import { HttpClient, HttpEvent, HttpHandlerFn, HttpInterceptorFn, HttpRequest, HttpResponse } from '@angular/common/http';
import { TestBed } from '@angular/core/testing';

fdescribe('AuthInterceptor', () => {
    const executeInterceptor: HttpInterceptorFn = (thisReq, thisNext) =>
        TestBed.runInInjectionContext(() => authInterceptor(thisReq, thisNext));

    let httpEventMock: jasmine.SpyObj<HttpResponse<unknown>>;
    let next: HttpHandlerFn;
    let userServiceMock: {
        userData: typeof UserService.prototype.userData,
        saveUserData: typeof UserService.prototype.saveUserData
    };
    let httpMock: jasmine.SpyObj<HttpClient>;

    beforeEach(() => {
        httpEventMock = jasmine.createSpyObj<HttpResponse<unknown>>([], ['statusText']);
        next = (req) => of({ ...httpEventMock, ...req, statusText: 'test success for ' + req.url });
        userServiceMock = {
            userData: signal({
                username: 'natevin',
                email: '123test@gmail.com',
                user_id: '12345678',
                profile: {
                    picture: null,
                    banner: null,
                    color: null,
                    theme: null
                },
                personal_stores: [],
                authentication: {
                    token: '123token',
                    refresh_token: '123refresh',
                    expiration: ((Date.now() / 1000) + 100) + ''
                }
            }),
            saveUserData: pipe(tap(console.log))
        };
        httpMock = jasmine.createSpyObj(['post']);
        TestBed.configureTestingModule({
            providers: [
                { provide: UserService, useValue: userServiceMock },
                { provide: HttpClient, useValue: httpMock }
            ]
        });
    });

    it('should have auth intercept for internal gql calls', () => {
        const reqGQL = new HttpRequest('POST', GQL_SERVER_URL, {});
        let resultGQL: HttpEvent<unknown> | undefined = undefined;
        executeInterceptor(reqGQL, next).subscribe({
            next: (data) => {
                resultGQL = data;
                expect((data as HttpResponse<unknown>).headers.has('X-Authentication-Token')).toBe(true);
            },
            error: fail
        });
        expect(resultGQL).toBeDefined();
    });

    it('should not have auth intercept for internal rest calls', () => {
        const reqREST = new HttpRequest('POST', REST_SERVER_URL, {});
        let resultREST: HttpEvent<unknown> | undefined = undefined;
        executeInterceptor(reqREST, next).subscribe({
            next: (data) => {
                resultREST = data;
                expect((data as HttpResponse<unknown>).headers.has('X-Authentication-Token')).toBe(false);
            },
            error: fail
        });
        expect(resultREST).toBeDefined();
    });

    it('should not have auth intercept for external calls', () => {
        const reqOther = new HttpRequest('POST', 'https://store.crunchyroll.com/', {});
        let resultOther: HttpEvent<unknown> | undefined = undefined;
        executeInterceptor(reqOther, next).subscribe({
            next: (data) => {
                resultOther = data;
                expect((data as HttpResponse<unknown>).headers.has('X-Authentication-Token')).toBe(false);
            },
            error: fail
        });
        expect(resultOther).toBeDefined();
    });
});
