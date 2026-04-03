import apiClient from "./client";

export const getAssociations = async () => {
    const response = await apiClient.get('/associations');
    return response.data;
}

