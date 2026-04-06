import apiClient from "./client";

export const getItems = async () => {
    const response = await apiClient.get('/items/');
    return response.data
}

export const getAssociationItems = async (associationId) => {
    const response = await apiClient.get(`/associations/${associationId}/items`);
    return response.data
}

