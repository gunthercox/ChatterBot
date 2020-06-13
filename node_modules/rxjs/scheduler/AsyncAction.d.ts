import { Action } from './Action';
import { Subscription } from '../Subscription';
import { AsyncScheduler } from './AsyncScheduler';
/**
 * We need this JSDoc comment for affecting ESDoc.
 * @ignore
 * @extends {Ignored}
 */
export declare class AsyncAction<T> extends Action<T> {
    protected scheduler: AsyncScheduler;
    id: any;
    state: T;
    delay: number;
    protected pending: boolean;
    protected work: (this: this, state?: T) => void;
    constructor(scheduler: AsyncScheduler, work: (this: AsyncAction<T>, state?: T) => void);
    schedule(state?: T, delay?: number): Subscription;
    protected requestAsyncId(scheduler: AsyncScheduler, id?: any, delay?: number): any;
    protected recycleAsyncId(scheduler: AsyncScheduler, id: any, delay?: number): any;
    /**
     * Immediately executes this action and the `work` it contains.
     * @return {any}
     */
    execute(state: T, delay: number): any;
    protected _execute(state: T, delay: number): any;
    /** @deprecated internal use only */ _unsubscribe(): void;
}
