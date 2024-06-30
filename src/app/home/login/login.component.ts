import { AsyncPipe, JsonPipe } from '@angular/common';
import { Component, DestroyRef, inject, model, signal } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { UserService } from '../../services/data/user.service';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Router } from '@angular/router';
import { HttpErrorResponse } from '@angular/common/http';
import { map, take } from 'rxjs';
import { LoginService } from '../../services/login.service';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
    selector: 'app-login',
    standalone: true,
    imports: [ReactiveFormsModule, JsonPipe, AsyncPipe],
    templateUrl: './login.component.html',
    styleUrl: './login.component.css'
})
export class LoginComponent {

    private readonly _userService = inject(UserService);
    private readonly _router = inject(Router);
    private readonly _destroyRef = inject(DestroyRef);
    private readonly _dialogRef = inject(MatDialogRef<LoginComponent>);

    protected readonly pathContext = inject<{ path: string; name: string; }>(MAT_DIALOG_DATA);

    test = model('');

    loginService = inject(LoginService);

    protected loginError = signal('');

    //#region Form
    protected userForm = new FormGroup({
        email: new FormControl('', [Validators.required, Validators.email]),
        username: new FormControl('', Validators.required),
        password: new FormControl('', [
            Validators.required,
            Validators.pattern(
                '(?=.*[A-Za-z])(?=.*[0-9])(?=.*[$@$!#^~%*?&,.<>"\'\\;:{\\}\\[\\]\\|\\+\\-\\=\\_\\)\\(\\)\\`\\/\\\\\\]])[A-Za-z0-9d$@].{7,}'
            )
        ]),
    });

    protected emailError$ = this.userForm.valueChanges.pipe(
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
        map(() => {
            if (!this.userForm.controls.username.touched || this.userForm.controls.username.valid) {
                return '';
            }
            if (this.userForm.controls.username.errors?.['required']) {
                return 'A username is required.';
            }
            return 'Your username must be at least 3 characters long.';
        })
    );

    protected passwordError$ = this.userForm.valueChanges.pipe(
        map(() => this.userForm.controls.password.touched && this.userForm.controls.password.invalid)
    );
    //#endregion

    /**
     * User login or sign up to get the user's auth token.
     * This is parameterized by the current path (login or sign-up).
     * If the login is successful, the user is redirected to the collection page.
     */
    protected login() {
        if (this.userForm.invalid) return;

        const { username, password } = this.userForm.value;

        this._userService.login(username!, password!, this.pathContext.path).pipe(
            takeUntilDestroyed(this._destroyRef),
            take(1)
        ).subscribe({
            next: (userData) => {
                this.loginError.set('');
                this._router.navigate(['collection'], { queryParams: { user_id: userData.user_id } });
            },
            error: (err: HttpErrorResponse) => {
                this.loginError.set(err.error.message);
            }
        });
    }

}
