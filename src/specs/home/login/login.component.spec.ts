import { ComponentFixture, fakeAsync, TestBed, tick } from '@angular/core/testing';
import { LoginComponent } from '../../../app/home/login/login.component';
import { DestroyRef, ChangeDetectorRef } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { LOGIN_PATH_CONTEXT, SIGNUP_PATH_CONTEXT, UserService } from '../../../app/services/data/user.service';

fdescribe('LoginComponent', () => {
    let component: LoginComponent;
    let fixture: ComponentFixture<LoginComponent>;

    let userServiceMock: jasmine.SpyObj<UserService>;
    let destroyRefMock: jasmine.SpyObj<DestroyRef>;
    let dialogRefMock: jasmine.SpyObj<MatDialogRef<LoginComponent>>;
    let cdrMock: jasmine.SpyObj<ChangeDetectorRef>;
    let matDialogDataMock: typeof LOGIN_PATH_CONTEXT;

    beforeEach(async () => {
        userServiceMock = jasmine.createSpyObj(['login', 'signUp']);
        destroyRefMock = jasmine.createSpyObj(['destroy']);
        dialogRefMock = jasmine.createSpyObj(['close']);
        cdrMock = jasmine.createSpyObj(['detectChanges']);
        matDialogDataMock = LOGIN_PATH_CONTEXT;
        await TestBed.configureTestingModule({
            imports: [LoginComponent],
            providers: [
                { provide: UserService, useValue: userServiceMock },
                { provide: DestroyRef, useValue: destroyRefMock },
                { provide: MatDialogRef, useValue: dialogRefMock },
                { provide: ChangeDetectorRef, useValue: cdrMock },
                { provide: MAT_DIALOG_DATA, useValue: matDialogDataMock }
            ]
        })
            .compileComponents();

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

    it('should not return an email error if it is untouched', fakeAsync(() => {
        let text: string | undefined;
        component['emailError$'].subscribe((error) => text = error);
        component['userForm'].controls.email.markAsUntouched();
        component['userForm'].controls.email.setValue('');
        tick(500);
        expect(text).toBe('');
    }));

    it('should not return an email error if it is valid', fakeAsync(() => {
        let text: string | undefined;
        component['emailError$'].subscribe((error) => text = error);
        component['userForm'].controls.email.markAsTouched();
        component['userForm'].controls.email.setValue('user@gmail.com');
        tick(500);
        expect(text).toBe('');
    }));

    it('should return an email error if it touched and empty', fakeAsync(() => {
        let text: string | undefined;
        component['emailError$'].subscribe((error) => text = error);
        component['userForm'].controls.email.markAsTouched();
        component['userForm'].controls.email.setValue('');
        tick(500);
        expect(text).toBe('An email address is required.');
    }));

    it('should return an email error if it is invalid', fakeAsync(() => {
        let text: string | undefined;
        component['emailError$'].subscribe((error) => text = error);
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
        component['emailError$'].subscribe((error) => text = error);
        component['userForm'].controls.email.markAsUntouched();
        component['userForm'].controls.email.setValue('');
        tick(499);
        expect(text).toBeUndefined();
        tick(1);
        expect(text).toBe('');
    }));

    it('should not return a username error if it is untouched', fakeAsync(() => {
        let text: string | undefined;
        component['usernameError$'].subscribe((error) => text = error);
        component['userForm'].controls.username.markAsUntouched();
        component['userForm'].controls.username.setValue('');
        tick(500);
        expect(text).toBe('');
    }));

    it('should not return an username error if it is valid', fakeAsync(() => {
        let text: string | undefined;
        component['usernameError$'].subscribe((error) => text = error);
        component['userForm'].controls.email.markAsTouched();
        component['userForm'].controls.username.setValue('usr');
        tick(500);
        expect(text).toBe('');
    }));

    it('should return an username error if it touched and empty', fakeAsync(() => {
        let text: string | undefined;
        component['usernameError$'].subscribe((error) => text = error);
        component['userForm'].controls.username.markAsTouched();
        const invalidUsernames = [null, ''];
        invalidUsernames.forEach(username => {
            component['userForm'].controls.username.setValue(username);
            tick(500);
            expect(text).toBe('A username is required.');
        });
    }));

    it('should return an username error if it is invalid', fakeAsync(() => {
        let text: string | undefined;
        component['usernameError$'].subscribe((error) => text = error);
        component['userForm'].controls.username.markAsTouched();
        const invalidUsernames = ['u', 'us'];
        invalidUsernames.forEach(username => {
            component['userForm'].controls.username.setValue(username);
            tick(500);
            expect(text).toBe('Your username must be at least 3 characters long.');
        });
    }));

    it('should not get a username error response until after 500 debounce', fakeAsync(() => {
        let text: string | undefined;
        component['usernameError$'].subscribe((error) => text = error);
        component['userForm'].controls.username.markAsUntouched();
        component['userForm'].controls.username.setValue('');
        tick(499);
        expect(text).toBeUndefined();
        tick(1);
        expect(text).toBe('');
    }));
});
