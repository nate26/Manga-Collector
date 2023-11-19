import { trigger, transition, style, animate } from '@angular/animations';
import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { Observable } from 'rxjs';
import { IManga } from '../../interfaces/iManga.interface';

@Component({
    selector: 'app-grid-view',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './grid-view.component.html',
    styleUrl: './grid-view.component.css',
    animations: [
        trigger('fade', [
            transition('false => true', [
                style({ opacity: 0 }),
                animate(400, style({ opacity: 1 }))
            ]),
            transition('true => false', [
                style({ opacity: 1 }),
                animate(400, style({ opacity: 0 }))
            ])
        ])
    ]
})
export class GridViewComponent implements OnInit {

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
