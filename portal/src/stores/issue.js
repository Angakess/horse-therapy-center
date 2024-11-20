import { defineStore } from "pinia";

export const useIssueStore = defineStore ('issues', {
    state: () => ({
        issues: [],
        loading: false,
        error: null,
    })
})