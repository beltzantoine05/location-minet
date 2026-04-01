import { Link } from "react-router-dom"
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

// On va utiliser ton propre logo comme "faux" logo pour toutes les assos pour l'instant !
import LogoAsso from "@/assets/minet_light.png"

// Nos données de test en attendant que le backend FastAPI nous les envoie plus tard
const associations = [
    { id: "1", name: "MiNET", description: "Câbles, serveurs et matériel informatique." },
    { id: "2", name: "BDE", description: "Sonos, tireuses, éco-cups et matériel de soirée." },
    { id: "3", name: "ASINT", description: "Matériel sportif et ballons." },
    { id: "4", name: "BDA", description: "Instruments de musique et matériel d'art." },
]

export default function Home() {
    return (
        <div className="container mx-auto px-4 max-w-7xl py-12">

            {/* L'en-tête de la page principale */}
            <div className="mb-12 text-center transition-all animate-in fade-in slide-in-from-bottom-4 duration-700">
                <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl mb-4">
                    À qui veux-tu louer ?
                </h1>
                <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
                    Sélectionne une association pour consulter son catalogue de matériel disponible à la location.
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
                                <img src={LogoAsso} alt={asso.name} className="h-14 w-14 object-contain" />
                            </div>
                            <CardTitle className="text-2xl font-bold">{asso.name}</CardTitle>
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
        </div>
    );
}
