import { Component, inject } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from '../../services/data/user.service';

@Component({
    selector: 'app-home',
    standalone: true,
    imports: [],
    templateUrl: './home.component.html',
    styleUrl: './home.component.css'
})
export class HomeComponent {

    private readonly router = inject(Router);
    protected readonly userService = inject(UserService);

    routeTo(path: string) {
        this.router.navigateByUrl(path);
    }

    routeToUserPage(path: string) {
        this.router.navigate([path], { queryParams: { user_id: localStorage.getItem('user_id') } });
    }
}
