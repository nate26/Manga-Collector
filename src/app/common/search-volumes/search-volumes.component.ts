import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { Observable } from 'rxjs';
import { IVolume } from '../../interfaces/iVolume.interface';
import { SearchService } from '../../services/data/search.service';
import { toObservable } from '@angular/core/rxjs-interop';

@Component({
    selector: 'app-search-volumes',
    standalone: true,
    imports: [
        CommonModule,
        FormsModule,
        MatFormFieldModule,
        MatInputModule,
        MatAutocompleteModule,
        ReactiveFormsModule
    ],
    templateUrl: './search-volumes.component.html',
    styleUrl: './search-volumes.component.css'
})
export class SearchVolumesComponent {

    searchText = '';

    search = signal('');
    searchResults$: Observable<IVolume[]> = toObservable(this.search).pipe(
        this.searchService.searchVolumes$
    );

    constructor(private searchService: SearchService) { }

}
