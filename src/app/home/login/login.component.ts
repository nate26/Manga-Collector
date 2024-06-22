import { HttpClient } from '@angular/common/http';
import { Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
    selector: 'app-login',
    standalone: true,
    imports: [FormsModule],
    templateUrl: './login.component.html',
    styleUrl: './login.component.css'
})
export class LoginComponent {

    http = inject(HttpClient);

    username = '';
    password = '';

    login() {
        this.http.post('http://localhost:8050/login', { username: this.username, password: this.password }).subscribe((res) => {
            console.log(res);
        });
    }

}
