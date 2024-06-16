import { Component, inject } from '@angular/core';
import { Router } from '@angular/router';

@Component({
    selector: 'app-home',
    standalone: true,
    imports: [],
    templateUrl: './home.component.html',
    styleUrl: './home.component.css'
})
export class HomeComponent {

    private readonly router = inject(Router);

    routeTo(path: string) {
        this.router.navigateByUrl(path);
    }
}
