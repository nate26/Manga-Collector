import { TitleCasePipe } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
    selector: 'app-login',
    standalone: true,
    imports: [FormsModule, TitleCasePipe],
    templateUrl: './login.component.html',
    styleUrl: './login.component.css'
})
export class LoginComponent {

    http = inject(HttpClient);

    route = 'login'

    username = '';
    password = '';
    token = '';

    nextRoute = () => this.route === 'login' ? 'sign-up' : 'login';
    switchRoute = () => this.route = this.nextRoute();

    login() {
        this.http.post<{ token: string }>(
            'http://localhost:8050/' + this.route,
            { username: this.username, password: this.password }
        ).subscribe((res) => {
            this.token = res.token;
        });
    }

    test() {
        this.http.get<string>(
            'http://localhost:8050/test',
            { headers: { Authorization: 'Bearer ' + this.token } }
        ).subscribe((res) => {
            console.log(res);
        });
    }

}
