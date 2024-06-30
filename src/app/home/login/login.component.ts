import { JsonPipe, TitleCasePipe } from '@angular/common';
import { Component, DestroyRef, computed, inject, signal } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { UserService } from '../../services/data/user.service';
import { takeUntilDestroyed, toSignal } from '@angular/core/rxjs-interop';
import { Router } from '@angular/router';
import { HttpErrorResponse } from '@angular/common/http';
import { take } from 'rxjs';

@Component({
    selector: 'app-login',
    standalone: true,
    imports: [ReactiveFormsModule, TitleCasePipe, JsonPipe],
    templateUrl: './login.component.html',
    styleUrl: './login.component.css'
})
export class LoginComponent {

    private readonly userService = inject(UserService);
    private readonly router = inject(Router);
    private readonly destroyRef = inject(DestroyRef);

    protected readonly _path = signal('login');
    protected nextRoute = computed(() => this._path() === 'login' ? 'sign-up' : 'login');

    protected loginError = signal('');

    userForm = new FormGroup({
        email: new FormControl('', [Validators.required, Validators.email]),
        username: new FormControl('', Validators.required),
        password: new FormControl('', [
            Validators.required,
            Validators.pattern(
                '(?=.*[A-Za-z])(?=.*[0-9])(?=.*[$@$!#^~%*?&,.<>"\'\\;:{\\}\\[\\]\\|\\+\\-\\=\\_\\)\\(\\)\\`\\/\\\\\\]])[A-Za-z0-9d$@].{7,}'
            )
        ]),
    });

    protected formChange = toSignal(this.userForm.valueChanges);

    protected emailError = computed(() => {
        this.formChange();
        if (!this.userForm.controls.email.touched || this.userForm.controls.email.valid) {
            return '';
        }
        if (this.userForm.controls.email.errors?.['required']) {
            return 'An valid email address is required.';
        }
        return 'Please provide a valid email address.';
    });

    protected usernameError = computed(() => {
        this.formChange();
        if (!this.userForm.controls.username.touched || this.userForm.controls.username.valid) {
            return '';
        }
        if (this.userForm.controls.username.errors?.['required']) {
            return 'A username is required.';
        }
        return 'Your username must be at least 3 characters long.';
    });

    protected passwordError = computed(() => {
        this.formChange();
        return this.userForm.controls.password.touched && this.userForm.controls.password.invalid;
    });

    /**
     * User login or sign up to get the user's auth token.
     * This is parameterized by the current path (login or sign-up).
     * If the login is successful, the user is redirected to the collection page.
     */
    protected login() {
        if (this.userForm.invalid) return;

        const { username, password } = this.userForm.value;

        this.userService.login(username!, password!, '/' + this._path()).pipe(
            takeUntilDestroyed(this.destroyRef),
            take(1)
        ).subscribe({
            next: (userData) => {
                this.loginError.set('');
                this.router.navigate(['collection'], { queryParams: { user_id: userData.user_id } });
            },
            error: (err: HttpErrorResponse) => {
                this.loginError.set(err.error.message);
            }
        });
    }

    /**
     * Switch between the login and sign-up pages.
     */
    protected switchRoute() {
        this._path.set(this.nextRoute())
    }

    // test() {
    //     this.http.get<string>(
    //         'http://localhost:8050/test',
    //         { headers: { Authorization: 'Bearer ' + this.token } }
    //     ).subscribe((res) => {
    //         console.log(res);
    //     });
    // }

}
