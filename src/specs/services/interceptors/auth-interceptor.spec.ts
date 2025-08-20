import { UserData, UserService } from '../../../app/services/data/user.service';
import { signal } from '@angular/core';
import { of, pipe, tap } from 'rxjs';
import { GQL_SERVER_URL, REST_SERVER_URL } from '../../../app/app.config';
import { authInterceptor } from '../../../app/services/interceptors/auth-interceptor';
import {
  HttpClient,
  HttpEvent,
  HttpHandlerFn,
  HttpInterceptorFn,
  HttpRequest,
  HttpResponse
} from '@angular/common/http';
import { TestBed } from '@angular/core/testing';

describe('AuthInterceptor', () => {
  const executeInterceptor: HttpInterceptorFn = (thisReq, thisNext) =>
    TestBed.runInInjectionContext(() => authInterceptor(thisReq, thisNext));

  let httpEventMock: jasmine.SpyObj<HttpResponse<unknown>>;
  let next: HttpHandlerFn;
  let userData: UserData;
  let userServiceMock: {
    userData: typeof UserService.prototype.userData;
    saveUserData: typeof UserService.prototype.saveUserData;
  };
  let httpMock: jasmine.SpyObj<HttpClient>;
  let consoleLogSpy: jasmine.Spy<typeof console.log>;

  beforeEach(() => {
    httpEventMock = jasmine.createSpyObj<HttpResponse<unknown>>([], ['statusText']);
    next = req => of({ ...httpEventMock, ...req, statusText: 'test success for ' + req.url });
    userData = {
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
        expiration: Date.now() / 1000 + 1000 + ''
      }
    };
    userServiceMock = {
      userData: signal(userData),
      saveUserData: pipe(tap(data => console.log(data)))
    };
    httpMock = jasmine.createSpyObj(['post']);
    TestBed.configureTestingModule({
      providers: [
        { provide: UserService, useValue: userServiceMock },
        { provide: HttpClient, useValue: httpMock }
      ]
    });
    consoleLogSpy = spyOn(window.console, 'log');
    httpMock.post.and.returnValue(of());
  });

  it('should have auth intercept for internal gql calls', () => {
    const reqGQL = new HttpRequest('POST', GQL_SERVER_URL, {});
    let resultGQL: HttpEvent<unknown> | undefined = undefined;
    executeInterceptor(reqGQL, next).subscribe({
      next: data => {
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
      next: data => {
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
      next: data => {
        resultOther = data;
        expect((data as HttpResponse<unknown>).headers.has('X-Authentication-Token')).toBe(false);
      },
      error: fail
    });
    expect(resultOther).toBeDefined();
  });

  it('should use existing token if it has not passed the expiration time', () => {
    const req = new HttpRequest('POST', GQL_SERVER_URL, {});
    userServiceMock.userData.set({
      ...userData,
      authentication: {
        ...userData.authentication,
        token: '123tokentest',
        expiration: Date.now() / 1000 + 1000 + ''
      }
    });
    let result: HttpEvent<unknown> | undefined = undefined;
    executeInterceptor(req, next).subscribe({
      next: data => {
        result = data;
        expect((data as HttpResponse<unknown>).headers.get('X-Authentication-Token')).toBe(
          '123tokentest'
        );
      },
      error: fail
    });
    expect(result).toBeDefined();
    expect(consoleLogSpy).not.toHaveBeenCalled();
  });

  it('should get new token if it has passed the expiration time', () => {
    const req = new HttpRequest('POST', GQL_SERVER_URL, {});
    const expiredExpiration = Date.now() / 1000 - 1000 + '';
    const newExpiration = Date.now() / 1000 + 1000 + '';
    const newUserData = {
      ...userData,
      username: 'natevin2',
      authentication: {
        token: '123tokentestold',
        refresh_token: '123refreshtest',
        expiration: expiredExpiration
      }
    };
    userServiceMock.userData.set(newUserData);
    httpMock.post.and.returnValue(
      of({
        token: '123tokentest',
        refresh_token: '123refreshtest',
        expiration: newExpiration
      })
    );
    let result: HttpEvent<unknown> | undefined = undefined;
    executeInterceptor(req, next).subscribe({
      next: data => {
        result = data;
        expect((data as HttpResponse<unknown>).headers.get('X-Authentication-Token')).toBe(
          '123tokentest'
        );
      },
      error: fail
    });
    expect(result).toBeDefined();
    expect(consoleLogSpy).toHaveBeenCalledOnceWith({
      ...newUserData,
      authentication: {
        token: '123tokentest',
        refresh_token: '123refreshtest',
        expiration: newExpiration
      }
    });
    expect(httpMock.post).toHaveBeenCalledOnceWith(REST_SERVER_URL + '/refreshToken', {
      username: 'natevin2',
      refresh_token: '123refreshtest'
    });
  });
});
