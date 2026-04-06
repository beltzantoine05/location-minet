import { Link } from "react-router-dom"
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { useEffect, useState } from 'react'
import { getAssociations } from "@/api/associations"
import { getItems, getAssociationItems } from "@/api/item"

// On va utiliser ton propre logo comme "faux" logo pour toutes les assos pour l'instant !
import LogoAsso from "@/assets/minet_light.png"

// Nos données de test en attendant que le backend FastAPI nous les envoie plus tard
export default function Home() {
    const [associations, setAssociations] = useState([])
    const [items, setItems] = useState([])

    useEffect(() => {
        const testerConnexionBackend = async () => {
            try {
                const dataAsso = await getAssociations();
                const Item = await getItems();
                setAssociations(dataAsso);
                setItems(Item);
            } catch (error) {
                console.log("Erreur de connexion", error);
            }
        }
        testerConnexionBackend();
    }, [])

    return (
        <div className="container mx-auto px-4 max-w-7xl py-12">

            {/* L'en-tête de la page principale */}
            <div className="mb-12 text-center transition-all animate-in fade-in slide-in-from-bottom-4 duration-700">
                <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl mb-4">
                    À qui veux-tu louer ?
                </h1>
                <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
                    Sélectionne une association ou un club pour consulter son catalogue de matériel disponible à la location.
                </p>
            </div>

            {/* La grille responsive avec nos "carrés" (Cards) */}
            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">

                {/* On génère une carte pour chaque association du tableau */}
                {associations.map((asso) => (
                    <Card
                        key={asso.id}
                        className="group overflow-hidden transition-all duration-300 hover:shadow-xl hover:-translate-y-1 hover:border-primary/50"
                    >
                        <CardHeader className="text-center pt-8 pb-4">
                            {/* Le Logo centré avec un léger effet de zoom au survol */}
                            <div className="mx-auto flex h-24 w-24 items-center justify-center rounded-full bg-muted/50 mb-4 transition-transform duration-300 group-hover:scale-110">
                                <img src={LogoAsso} alt={asso.nom} className="h-14 w-14 object-contain" />
                            </div>
                            <CardTitle className="text-2xl font-bold">{asso.nom}</CardTitle>
                        </CardHeader>

                        <CardContent className="text-center text-sm text-muted-foreground min-h-[4rem]">
                            {asso.description}
                        </CardContent>

                        <CardFooter className="flex justify-center pb-8">
                            <Button asChild variant="default" className="w-full">
                                {/* Le lien qui mènera plus tard vers le catalogue spécifique à l'asso */}
                                <Link to={`/asso/${asso.id}`}>Voir le catalogue</Link>
                            </Button>
                        </CardFooter>
                    </Card>
                ))}
            </div>
            <div className="mt-12 text-center text-muted-foreground">
                Tu n'as pas trouvé ce que tu cherches ? <Link to="/contact" className="text-primary font-semibold hover:underline">Contacte-nous !</Link>
            </div>
        </div>
    );
}
