import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Observable } from 'rxjs';
import { IManga } from '../../interfaces/iManga.interface';

@Component({
    selector: 'app-list-view',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './list-view.component.html',
    styleUrl: './list-view.component.css'
})
export class ListViewComponent implements OnInit {

    @Input()
    volumes$!: Observable<IManga[]>;

    @Output()
    editVolume = new EventEmitter<IManga>();

    constructor() { }

    ngOnInit(): void {
    }

    edit(vol: IManga) {
        this.editVolume.emit(vol)
    }

}
