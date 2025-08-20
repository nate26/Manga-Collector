import { TestBed } from '@angular/core/testing';
import {
  ActivatedRouteSnapshot,
  CanActivateFn,
  Router,
  RouterStateSnapshot
} from '@angular/router';
import { loggedInGuard } from '../../app/guards/logged-in.guard';
import { UserData, UserDataPartial, UserService } from '../../app/services/data/user.service';
import { LoginService } from '../../app/services/login.service';
import { signal, WritableSignal } from '@angular/core';
import { Observable, of } from 'rxjs';

describe('loggedInGuard', () => {
  const executeGuard: CanActivateFn = (...guardParameters) =>
    TestBed.runInInjectionContext(() => loggedInGuard(...guardParameters));

  let loginServiceMock: jasmine.SpyObj<LoginService>;
  let routerMock: jasmine.SpyObj<Router>;
  let userServiceMock: jasmine.SpyObj<UserService>;

  let userDataMock: WritableSignal<UserDataPartial>;

  beforeEach(() => {
    loginServiceMock = jasmine.createSpyObj(['openLogin']);
    routerMock = jasmine.createSpyObj(['navigate']);
    userDataMock = signal({ username: null } as UserDataPartial);
    userServiceMock = {
      ...jasmine.createSpyObj(['userDataIsValid']),
      userData: userDataMock
    };
    TestBed.configureTestingModule({
      providers: [
        { provide: LoginService, useValue: loginServiceMock },
        { provide: Router, useValue: routerMock },
        { provide: UserService, useValue: userServiceMock }
      ]
    });
    loginServiceMock.openLogin.and.returnValue(of());
  });

  it('should navigate to /collection if you are logged without a provided user', () => {
    userServiceMock.userDataIsValid.and.returnValue(true);
    userDataMock.set({ username: 'testuser' } as UserData);

    const result = executeGuard(
      {} as ActivatedRouteSnapshot,
      { url: '/collection' } as RouterStateSnapshot
    );

    expect(routerMock.navigate).toHaveBeenCalledWith(['collection'], {
      queryParams: { username: 'testuser' }
    });
    expect(result).toBeTrue();
  });

  it('should navigate to /series if you are logged without a provided user', () => {
    userServiceMock.userDataIsValid.and.returnValue(true);
    userDataMock.set({ username: 'testuser' } as UserData);

    const result = executeGuard(
      {} as ActivatedRouteSnapshot,
      { url: '/series' } as RouterStateSnapshot
    );

    expect(routerMock.navigate).toHaveBeenCalledWith(['series'], {
      queryParams: { username: 'testuser' }
    });
    expect(result).toBeTrue();
  });

  it('should allow you to go to page if youre logged in and another user is specified', () => {
    userServiceMock.userDataIsValid.and.returnValue(true);
    userDataMock.set({ username: 'testuser' } as UserData);

    ['/collection?username=someuser', '/series?username=someuser'].forEach(url => {
      const result = executeGuard({} as ActivatedRouteSnapshot, { url } as RouterStateSnapshot);
      expect(result).toBeTrue();
    });

    expect(routerMock.navigate).not.toHaveBeenCalled();
  });

  it('should allow you to go to page if you are not logged in, but a user is specified', () => {
    userServiceMock.userDataIsValid.and.returnValue(false);
    userDataMock.set({ username: null } as UserDataPartial);

    ['/collection?username=someuser', '/series?username=someuser'].forEach(url => {
      const result = executeGuard({} as ActivatedRouteSnapshot, { url } as RouterStateSnapshot);
      expect(result).toBeTrue();
    });

    expect(routerMock.navigate).not.toHaveBeenCalled();
  });

  it('should not allow you to go to page if the other user is blank', () => {
    userServiceMock.userDataIsValid.and.returnValue(true);
    userDataMock.set({ username: 'testuser' } as UserData);

    ['/collection?username=', '/series?username='].forEach((url, i) => {
      const result = executeGuard({} as ActivatedRouteSnapshot, { url } as RouterStateSnapshot);
      expect(result).toBeInstanceOf(Observable);
      expect(loginServiceMock.openLogin).toHaveBeenCalledTimes(i + 1);
    });

    expect(routerMock.navigate).not.toHaveBeenCalled();
  });

  it('should open login window if you are not logged in and did not specify a user', () => {
    userServiceMock.userDataIsValid.and.returnValue(false);
    userDataMock.set({ username: null } as UserDataPartial);
    loginServiceMock.openLogin.and.returnValue(of({ username: '123test' } as UserData));

    const paths = ['/collection', '/series', '/collection?username=', '/series?username='];
    const expectedUrls = ['collection', 'series', 'collection', 'series'];

    paths.forEach((url, i) => {
      const result = executeGuard({} as ActivatedRouteSnapshot, { url } as RouterStateSnapshot);
      expect(result).toBeInstanceOf(Observable);
      expect(loginServiceMock.openLogin).toHaveBeenCalledTimes(i + 1);

      let obsResult: boolean | undefined = undefined;
      (result as Observable<boolean>).subscribe({
        next: data => (obsResult = data),
        error: fail
      });
      expect(obsResult).toBeTrue();
      expect(routerMock.navigate).toHaveBeenCalledTimes(i + 1);
      expect(routerMock.navigate.calls.allArgs()[i]).toEqual([
        [expectedUrls[i]],
        { queryParams: { username: '123test' } }
      ]);
    });
  });

  it('should open login window but not route if it is canceled without a user', () => {
    userServiceMock.userDataIsValid.and.returnValue(false);
    userDataMock.set({ username: null } as UserDataPartial);
    loginServiceMock.openLogin.and.returnValue(of(undefined));

    const paths = ['/collection', '/series'];

    paths.forEach((url, i) => {
      const result = executeGuard({} as ActivatedRouteSnapshot, { url } as RouterStateSnapshot);
      expect(result).toBeInstanceOf(Observable);
      expect(loginServiceMock.openLogin).toHaveBeenCalledTimes(i + 1);

      let obsResult: boolean | undefined = undefined;
      (result as Observable<boolean>).subscribe({
        next: data => (obsResult = data),
        error: fail
      });
      expect(obsResult).toBeUndefined();
    });
    expect(routerMock.navigate).not.toHaveBeenCalled();
  });
});
