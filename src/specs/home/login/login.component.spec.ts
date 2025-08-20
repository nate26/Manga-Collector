import { ComponentFixture, fakeAsync, TestBed, tick } from '@angular/core/testing';
import { LoginComponent } from '../../../app/home/login/login.component';
import { DestroyRef } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import {
  LOGIN_PATH_CONTEXT,
  SIGNUP_PATH_CONTEXT,
  UserData,
  UserService
} from '../../../app/services/data/user.service';
import { of, throwError } from 'rxjs';

describe('LoginComponent', () => {
  let component: LoginComponent;
  let fixture: ComponentFixture<LoginComponent>;

  let userServiceMock: jasmine.SpyObj<UserService>;
  let destroyRefMock: jasmine.SpyObj<DestroyRef>;
  let dialogRefMock: jasmine.SpyObj<MatDialogRef<LoginComponent>>;
  let matDialogDataMock: typeof LOGIN_PATH_CONTEXT;

  beforeEach(async () => {
    userServiceMock = jasmine.createSpyObj(['login', 'signUp']);
    destroyRefMock = jasmine.createSpyObj(['destroy']);
    dialogRefMock = jasmine.createSpyObj(['close']);
    matDialogDataMock = LOGIN_PATH_CONTEXT;
    await TestBed.configureTestingModule({
      imports: [LoginComponent],
      providers: [
        { provide: UserService, useValue: userServiceMock },
        { provide: DestroyRef, useValue: destroyRefMock },
        { provide: MatDialogRef, useValue: dialogRefMock },
        { provide: MAT_DIALOG_DATA, useValue: matDialogDataMock }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(LoginComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should check if path is login', () => {
    expect(component['isPathLogin']()).toBeTrue();
    component['pathContext'].set(LOGIN_PATH_CONTEXT);
    expect(component['isPathLogin']()).toBeTrue();
  });

  it('should check if path is sign up', () => {
    component['pathContext'].set(SIGNUP_PATH_CONTEXT);
    expect(component['isPathLogin']()).toBeFalse();
  });

  //#region email validators
  it('should not return an email error if it is untouched', fakeAsync(() => {
    let text: string | undefined;
    component['emailError$'].subscribe(error => (text = error));
    component['userForm'].controls.email.markAsUntouched();
    component['userForm'].controls.email.setValue('');
    tick(500);
    expect(text).toBe('');
  }));

  it('should not return an email error if it is valid', fakeAsync(() => {
    let text: string | undefined;
    component['emailError$'].subscribe(error => (text = error));
    component['userForm'].controls.email.markAsTouched();
    component['userForm'].controls.email.setValue('user@gmail.com');
    tick(500);
    expect(text).toBe('');
  }));

  it('should return an email error if it touched and empty', fakeAsync(() => {
    let text: string | undefined;
    component['emailError$'].subscribe(error => (text = error));
    component['userForm'].controls.email.markAsTouched();
    component['userForm'].controls.email.setValue('');
    tick(500);
    expect(text).toBe('An email address is required.');
  }));

  it('should return an email error if it is invalid', fakeAsync(() => {
    let text: string | undefined;
    component['emailError$'].subscribe(error => (text = error));
    component['userForm'].controls.email.markAsTouched();
    const invalidEmails = ['user', 'user.com', 'user@gmail', 'user@gmail.'];
    invalidEmails.forEach(email => {
      component['userForm'].controls.email.setValue(email);
      tick(500);
      expect(text).toBe('Please provide a valid email address.');
    });
  }));

  it('should not get an email error response until after 500 debounce', fakeAsync(() => {
    let text: string | undefined;
    component['emailError$'].subscribe(error => (text = error));
    component['userForm'].controls.email.markAsUntouched();
    component['userForm'].controls.email.setValue('');
    tick(499);
    expect(text).toBeUndefined();
    tick(1);
    expect(text).toBe('');
  }));
  //#endregion

  //#region username validators
  it('should not return a username error if it is untouched', fakeAsync(() => {
    component['pathContext'].set(SIGNUP_PATH_CONTEXT);
    let text: string | undefined;
    component['usernameError$'].subscribe(error => (text = error));
    component['userForm'].controls.username.markAsUntouched();
    component['userForm'].controls.username.setValue('');
    tick(500);
    expect(text).toBe('');
  }));

  it('should not return an username error on the login path', fakeAsync(() => {
    component['pathContext'].set(LOGIN_PATH_CONTEXT);
    let text: string | undefined;
    component['usernameError$'].subscribe(error => (text = error));
    component['userForm'].controls.username.markAsTouched();
    component['userForm'].controls.username.setValue('');
    tick(500);
    expect(text).toBe('');
  }));

  it('should not return an username error if it is valid', fakeAsync(() => {
    component['pathContext'].set(SIGNUP_PATH_CONTEXT);
    let text: string | undefined;
    component['usernameError$'].subscribe(error => (text = error));
    component['userForm'].controls.username.markAsTouched();
    component['userForm'].controls.username.setValue('usr');
    tick(500);
    expect(text).toBe('');
  }));

  it('should return an username error if it touched and empty', fakeAsync(() => {
    component['pathContext'].set(SIGNUP_PATH_CONTEXT);
    let text: string | undefined;
    component['usernameError$'].subscribe(error => (text = error));
    component['userForm'].controls.username.markAsTouched();
    const invalidUsernames = [null, ''];
    invalidUsernames.forEach(username => {
      component['userForm'].controls.username.setValue(username);
      tick(500);
      expect(text).toBe('A username is required.');
    });
  }));

  it('should return an username error if it is invalid', fakeAsync(() => {
    component['pathContext'].set(SIGNUP_PATH_CONTEXT);
    let text: string | undefined;
    component['usernameError$'].subscribe(error => (text = error));
    component['userForm'].controls.username.markAsTouched();
    const invalidUsernames = ['u', 'us'];
    invalidUsernames.forEach(username => {
      component['userForm'].controls.username.setValue(username);
      tick(500);
      expect(text).toBe('Your username must be at least 3 characters.');
    });
  }));

  it('should not get a username error response until after 500 debounce', fakeAsync(() => {
    component['pathContext'].set(SIGNUP_PATH_CONTEXT);
    let text: string | undefined;
    component['usernameError$'].subscribe(error => (text = error));
    component['userForm'].controls.username.markAsUntouched();
    component['userForm'].controls.username.setValue('');
    tick(499);
    expect(text).toBeUndefined();
    tick(1);
    expect(text).toBe('');
  }));
  //#endregion

  //#region password validators
  it('should not return a password error if it is empty', fakeAsync(() => {
    let text: string | undefined;
    component['passwordError$'].subscribe(error => (text = error));
    component['userForm'].controls.password.markAsTouched();
    component['userForm'].controls.password.setValue('');
    tick(500);
    expect(text).toBe('');
  }));
  it('should not return a password error if it is untouched', fakeAsync(() => {
    let text: string | undefined;
    component['passwordError$'].subscribe(error => (text = error));
    component['userForm'].controls.password.markAsUntouched();
    component['userForm'].controls.password.setValue('');
    tick(500);
    expect(text).toBe('');
  }));

  it('should not return an password error if it is valid', fakeAsync(() => {
    let text: string | undefined;
    component['passwordError$'].subscribe(error => (text = error));
    component['userForm'].controls.password.markAsTouched();
    component['userForm'].controls.password.setValue('123Apples!');
    tick(500);
    expect(text).toBe('');
  }));

  it('should return an password error if there are no capital letters', fakeAsync(() => {
    let text: string | undefined;
    component['passwordError$'].subscribe(error => (text = error));
    component['userForm'].controls.password.markAsTouched();
    component['userForm'].controls.password.setValue('123apples!');
    tick(500);
    expect(text).toBe('Password must contain at least one capital letter.');
  }));

  it('should return an password error if there are no numbers letters', fakeAsync(() => {
    let text: string | undefined;
    component['passwordError$'].subscribe(error => (text = error));
    component['userForm'].controls.password.markAsTouched();
    component['userForm'].controls.password.setValue('Appples!');
    tick(500);
    expect(text).toBe('Password must contain at least one number.');
  }));

  it('should return an password error if it is less than 8 characters long', fakeAsync(() => {
    let text: string | undefined;
    component['passwordError$'].subscribe(error => (text = error));
    component['userForm'].controls.password.markAsTouched();
    component['userForm'].controls.password.setValue('1Apple!');
    tick(500);
    expect(text).toBe('Password must be at least 8 characters long.');
  }));

  it('should return an password error if there are no special characters', fakeAsync(() => {
    let text: string | undefined;
    component['passwordError$'].subscribe(error => (text = error));
    component['userForm'].controls.password.markAsTouched();
    component['userForm'].controls.password.setValue('123Apples');
    tick(500);
    expect(text).toBe('Password must contain a special character.');
  }));

  it('should not get a password error response until after 500 debounce', fakeAsync(() => {
    let text: string | undefined;
    component['passwordError$'].subscribe(error => (text = error));
    component['userForm'].controls.password.markAsUntouched();
    component['userForm'].controls.password.setValue('');
    tick(499);
    expect(text).toBeUndefined();
    tick(1);
    expect(text).toBe('');
  }));
  //#endregion

  //#region Actions
  it('should not login or signup user with invalid email', () => {
    component['userForm'].controls.email.markAsTouched();
    component['userForm'].controls.email.setValue('');
    component['login']();
    expect(userServiceMock.login).not.toHaveBeenCalled();
    expect(userServiceMock.signUp).not.toHaveBeenCalled();
  });

  it('should not login or signup user with invalid username', () => {
    component['userForm'].controls.username.markAsTouched();
    component['userForm'].controls.username.setValue('');
    component['login']();
    expect(userServiceMock.login).not.toHaveBeenCalled();
    expect(userServiceMock.signUp).not.toHaveBeenCalled();
  });

  it('should not login or signup user with invalid password', () => {
    component['userForm'].controls.password.markAsTouched();
    component['userForm'].controls.password.setValue('');
    component['login']();
    expect(userServiceMock.login).not.toHaveBeenCalled();
    expect(userServiceMock.signUp).not.toHaveBeenCalled();
  });

  it('should login user', () => {
    component['userForm'].controls.email.markAsTouched();
    component['userForm'].controls.email.setValue('user@gmail.com');
    component['userForm'].controls.password.markAsTouched();
    component['userForm'].controls.password.setValue('123Apple!');
    userServiceMock.login.and.returnValue(
      of({
        email: 'user@gmail.com',
        username: 'user'
      } as UserData)
    );

    component['pathContext'].set(LOGIN_PATH_CONTEXT);
    component['login']();

    expect(userServiceMock.login).toHaveBeenCalledOnceWith('user@gmail.com', '123Apple!');
    expect(component['loginError']()).toBe('');
    expect(dialogRefMock.close).toHaveBeenCalledOnceWith({
      email: 'user@gmail.com',
      username: 'user'
    } as UserData);
  });

  it('should not login user with a service error', () => {
    component['userForm'].controls.email.markAsTouched();
    component['userForm'].controls.email.setValue('user@gmail.com');
    component['userForm'].controls.password.markAsTouched();
    component['userForm'].controls.password.setValue('123Apple!');
    userServiceMock.login.and.returnValue(
      throwError(() => ({ error: Error('Invalid email or password.') }))
    );

    component['pathContext'].set(LOGIN_PATH_CONTEXT);
    component['login']();

    expect(userServiceMock.login).toHaveBeenCalledOnceWith('user@gmail.com', '123Apple!');
    expect(component['loginError']()).toBe('Invalid email or password.');
    expect(dialogRefMock.close).not.toHaveBeenCalled();
  });

  it('should signup user', () => {
    component['userForm'].controls.email.markAsTouched();
    component['userForm'].controls.email.setValue('user@gmail.com');
    component['userForm'].controls.username.markAsTouched();
    component['userForm'].controls.username.setValue('user');
    component['userForm'].controls.password.markAsTouched();
    component['userForm'].controls.password.setValue('123Apple!');
    userServiceMock.signUp.and.returnValue(
      of({
        email: 'user@gmail.com',
        username: 'user'
      } as UserData)
    );

    component['pathContext'].set(SIGNUP_PATH_CONTEXT);
    component['login']();

    expect(userServiceMock.signUp).toHaveBeenCalledOnceWith('user@gmail.com', 'user', '123Apple!');
    expect(component['loginError']()).toBe('');
    expect(dialogRefMock.close).toHaveBeenCalledOnceWith({
      email: 'user@gmail.com',
      username: 'user'
    } as UserData);
  });

  it('should not signup user with a service error', () => {
    component['userForm'].controls.email.markAsTouched();
    component['userForm'].controls.email.setValue('user@gmail.com');
    component['userForm'].controls.username.markAsTouched();
    component['userForm'].controls.username.setValue('user');
    component['userForm'].controls.password.markAsTouched();
    component['userForm'].controls.password.setValue('123Apple!');
    userServiceMock.signUp.and.returnValue(
      throwError(() => ({ error: Error('Invalid email or password.') }))
    );

    component['pathContext'].set(SIGNUP_PATH_CONTEXT);
    component['login']();

    expect(userServiceMock.signUp).toHaveBeenCalledOnceWith('user@gmail.com', 'user', '123Apple!');
    expect(component['loginError']()).toBe('Invalid email or password.');
    expect(dialogRefMock.close).not.toHaveBeenCalled();
  });

  it('should switch path to sign up', () => {
    component['pathContext'].set(LOGIN_PATH_CONTEXT);
    component['switchPath']();
    expect(component['pathContext']()).toBe(SIGNUP_PATH_CONTEXT);
  });

  it('should switch path to login', () => {
    component['pathContext'].set(SIGNUP_PATH_CONTEXT);
    component['userForm'].controls.username.setValue('user');
    component['switchPath']();
    expect(component['pathContext']()).toBe(LOGIN_PATH_CONTEXT);
    expect(component['userForm'].controls.username.value).toBeNull();
  });

  it('should close login dialog', () => {
    component['closeLogin']();
    expect(dialogRefMock.close).toHaveBeenCalledTimes(1);
  });
  //#endregion

  //#region template
  it('should display username on signup window', () => {
    component['pathContext'].set(SIGNUP_PATH_CONTEXT);
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelector('#username-form')).toBeTruthy();
  });

  it('should not display username on login window', () => {
    component['pathContext'].set(LOGIN_PATH_CONTEXT);
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelector('#username-form')).toBeNull();
  });

  it('should display Sign Up link on login window', () => {
    component['pathContext'].set(LOGIN_PATH_CONTEXT);
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelector('#login-nav-link').textContent.trim()).toBe(
      "Don't have an account? Sign up here."
    );
  });

  it('should display Login link on signup window', () => {
    component['pathContext'].set(SIGNUP_PATH_CONTEXT);
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelector('#login-nav-link').textContent.trim()).toBe(
      'Already have an account? Login here.'
    );
  });
  //#endregion
});
