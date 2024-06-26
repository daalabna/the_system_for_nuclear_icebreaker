import {IGrade, IIcebreaker, IVessel, tModal, TypeSidebar} from "../../types.ts";

export namespace CommonStore {
    export type Id = 'CommonStore'

    export interface State {
        openModal: boolean
        typeModal: tModal | null
        modalInfo: IVessel | IIcebreaker | null

        showGraph: boolean

        typeSidebar: TypeSidebar

        isLoading: boolean

        grade: IGrade | null
    }

    export interface Actions {
        getGrade(): (template: string) => Promise<void>
    }
}
