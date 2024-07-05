import { AsyncPipe, JsonPipe, NgTemplateOutlet } from '@angular/common';
import { Component, DestroyRef, computed, inject, signal } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { UserService } from '../../services/data/user.service';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Router } from '@angular/router';
import { HttpErrorResponse } from '@angular/common/http';
import { debounceTime, map, take } from 'rxjs';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

export const LOGIN_PATH_CONTEXT = {
    path: '/login',
    name: 'Login'
};

export const SIGNUP_PATH_CONTEXT = {
    path: '/sign-up',
    name: 'Sign Up'
};

@Component({
    selector: 'app-login',
    standalone: true,
    imports: [ReactiveFormsModule, JsonPipe, AsyncPipe, NgTemplateOutlet],
    templateUrl: './login.component.html',
    styleUrl: './login.component.css'
})
export class LoginComponent {

    private readonly _userService = inject(UserService);
    private readonly _router = inject(Router);
    private readonly _destroyRef = inject(DestroyRef);
    private readonly _dialogRef = inject(MatDialogRef<LoginComponent>);

    protected readonly pathContext = signal(inject<typeof LOGIN_PATH_CONTEXT>(MAT_DIALOG_DATA));
    protected readonly isPathLogin = computed(() => this.pathContext().path === LOGIN_PATH_CONTEXT.path);

    //#region Form
    protected userForm = new FormGroup({
        email: new FormControl('', [Validators.required, Validators.email]),
        username: new FormControl(null),
        password: new FormControl('', [
            Validators.required,
            Validators.pattern(
                '(?=.*[A-Za-z])(?=.*[0-9])(?=.*[$@$!#^~%*?&,.<>"\'\\;:{\\}\\[\\]\\|\\+\\-\\=\\_\\)\\(\\)\\`\\/\\\\\\]])[A-Za-z0-9d$@].{8,}'
            )
        ]),
    });
    //#endregion

    protected loginError = signal('');
    private readonly USERNAME_VALIDATORS = [Validators.required, Validators.minLength(3)];

    //#region Validators
    protected emailError$ = this.userForm.valueChanges.pipe(
        debounceTime(1500),
        map(() => {
            if (!this.userForm.controls.email.touched || this.userForm.controls.email.valid) {
                return '';
            }
            if (this.userForm.controls.email.errors?.['required']) {
                return 'An valid email address is required.';
            }
            return 'Please provide a valid email address.';
        })
    );

    protected usernameError$ = this.userForm.valueChanges.pipe(
        debounceTime(1500),
        map(() => {
            if (!this.userForm.controls.username.touched || this.userForm.controls.username.valid) {
                return '';
            }
            if (this.userForm.controls.username.errors?.['required']) {
                return 'A username is required.';
            }
            if (this.userForm.controls.username.errors?.['minlength']) {
                return 'Your username must be at least 3 characters long.';
            }
            return 'Your username must be at least 3 characters long.';
        })
    );

    protected passwordError$ = this.userForm.valueChanges.pipe(
        debounceTime(1500),
        map(() => {
            const value = this.userForm.controls.password.value;
            if (!value || !this.userForm.controls.password.touched || this.userForm.controls.password.valid) {
                return '';
            }
            if (!RegExp('.*[A-Z].*').test(value)) {
                return 'Password must contain at least one capital letter.';
            }
            if (!RegExp('.*[0-9].*').test(value)) {
                return 'Password must contain at least one number.';
            }
            if (!RegExp('.{8,}').test(value)) {
                return 'Password must be at least 8 characters long.';
            }
            return 'Password must contain a special character.';
        })
    );
    //#endregion

    /**
     * User login or sign up to get the user's auth token.
     * This is parameterized by the current path (login or sign-up).
     * If the login is successful, the user is redirected to the collection page.
     */
    protected login(): void {
        if (this.userForm.invalid) return;

        const { username, password, email } = this.userForm.value;

        this._userService.login(username!, password!, email!, this.pathContext().path).pipe(
            takeUntilDestroyed(this._destroyRef),
            take(1)
        ).subscribe({
            next: (userData) => {
                this.loginError.set('');
                this._router.navigate(['collection'], { queryParams: { user_id: userData.user_id } });
                this._dialogRef.close(true);
            },
            error: (err: HttpErrorResponse) => {
                this.loginError.set(err.error.message);
            }
        });
    }

    protected switchPath() {
        if (this.isPathLogin()) {
            this.pathContext.set(SIGNUP_PATH_CONTEXT);
            this.userForm.controls.username.setValidators(this.USERNAME_VALIDATORS);
        }
        else {
            this.pathContext.set(LOGIN_PATH_CONTEXT);
            this.userForm.controls.username.setValue(null);
            this.userForm.controls.username.setValidators([]);
        }
    }

}
