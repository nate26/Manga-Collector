import { Component, input, signal } from '@angular/core';
import { ControlValueAccessor, NG_VALUE_ACCESSOR } from '@angular/forms';
import { MatSliderModule } from '@angular/material/slider';

export type NumberRange = {
    min?: number | null;
    max?: number | null;
};

@Component({
    selector: 'app-number-range-filter',
    standalone: true,
    imports: [MatSliderModule],
    providers: [
        {
            provide: NG_VALUE_ACCESSOR,
            multi: true,
            useExisting: NumberRangeFilterComponent
        }
    ],
    templateUrl: './number-range-filter.component.html',
    styleUrl: './number-range-filter.component.css'
})
export class NumberRangeFilterComponent implements ControlValueAccessor {
    title = input.required<string>();
    min = input<number>(0);
    max = input<number>(100);
    step = input<number>(0.01);

    minValue = signal<number | null | undefined>(null);
    maxValue = signal<number | null | undefined>(null);

    disabled = signal(false);

    onChange: (_: NumberRange) => void = () => {};
    onTouch = () => {};

    updateMin($event: Event) {
        const val = ($event.target as HTMLInputElement).valueAsNumber;
        this.minValue.set(val <= this.min() ? null : val);
        this.processOnChange();
    }

    updateMax($event: Event) {
        const val = ($event.target as HTMLInputElement).valueAsNumber;
        this.maxValue.set(val >= this.max() ? null : val);
        this.processOnChange();
    }

    processOnChange() {
        this.onChange({
            min: this.minValue(),
            max: this.maxValue()
        });
    }

    writeValue(obj: NumberRange): void {
        this.minValue.set(obj?.min);
        this.maxValue.set(obj?.max);
    }

    registerOnChange(fn: (_: NumberRange) => void): void {
        this.onChange = fn;
    }

    registerOnTouched(fn: () => void): void {
        this.onTouch = fn;
    }

    setDisabledState?(isDisabled: boolean): void {
        this.disabled.set(isDisabled);
    }
}
