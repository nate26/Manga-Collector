import { TitleCasePipe } from '@angular/common';
import { Component, DestroyRef, computed, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { UserService } from '../../services/data/user.service';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpErrorResponse } from '@angular/common/http';
import { take } from 'rxjs';

@Component({
    selector: 'app-login',
    standalone: true,
    imports: [FormsModule, TitleCasePipe],
    templateUrl: './login.component.html',
    styleUrl: './login.component.css'
})
export class LoginComponent {

    private readonly userService = inject(UserService);
    private readonly router = inject(Router);
    private readonly activatedRoute = inject(ActivatedRoute);
    private readonly destroyRef = inject(DestroyRef);

    protected readonly _path = signal('login');
    protected nextRoute = computed(() => this._path() === 'login' ? 'sign-up' : 'login');

    protected loginError = signal('');

    protected username = '';
    protected password = '';

    /**
     * User login or sign up to get the user's auth token.
     * This is parameterized by the current path (login or sign-up).
     * If the login is successful, the user is redirected to the collection page.
     */
    protected login() {
        this.userService.login(this.username, this.password, '/' + this._path()).pipe(
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
