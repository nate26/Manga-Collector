import { Component, inject } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from '../../services/data/user.service';
import { LoginService } from '../../services/login.service';

@Component({
    selector: 'app-home',
    standalone: true,
    imports: [],
    templateUrl: './home.component.html',
    styleUrl: './home.component.css'
})
export class HomeComponent {

    private readonly _router = inject(Router);
    private readonly _loginService = inject(LoginService);
    protected readonly userService = inject(UserService);

    routeTo(path: string) {
        this._router.navigateByUrl(path);
    }

    routeToUserPage(path: string) {
        this._router.navigate([path], { queryParams: { username: localStorage.getItem('username') } });
    }

    callOpenLogin() {
        this._loginService.openLogin().subscribe();
    }

}
