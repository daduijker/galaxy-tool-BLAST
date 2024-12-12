class Generic:

    def find_generic_taxonomy(self, line):
        taxonomyList = line.split("\t")[1].split("|")[2].split(";")
        databaseSource = line.split("\t")[1].split("|")[0].strip(">")
        print(taxonomyList)
        species = taxonomyList[-1] if taxonomyList[-1] else "unknown species"
        species = species.replace("_", " ")
        genus = taxonomyList[-2] if taxonomyList[-2] else "unknown genus"
        family = taxonomyList[-3] if taxonomyList[-3] else "unknown family"
        order = taxonomyList[-4] if taxonomyList[-4] else "unknown order"
        classe = taxonomyList[-5] if taxonomyList[-5] else "unknown class"
        phylum = taxonomyList[-6] if taxonomyList[-6] else "unknown phylum"
        kingdom = taxonomyList[-7] if taxonomyList[-7] else "unknown kingdom"
        superkingdom = taxonomyList[-8] if taxonomyList[-8] else "unknown superkingdom"
        taxonomy = [kingdom, phylum, classe, order, family, genus, species]

        newLine = line.strip().split("\t")
        print(newLine[1])
        if len(line.split("\t")[1].split("|")) == 4:
            newLine[1] = newLine[1].split("|")[1]+"|"+line.split("\t")[1].split("|")[3]
        else:
            newLine[1] = newLine[1].split("|")[1]+"|N/A"
        #newLine[2] = newLine[1].split("|")[2]+"|"+newLine[1].split("|")[3]
        newLine[2] = newLine[1].split("|")[0]
        
        if len(line.split("\t")[1].split("|")) == 4:
            newLine[3] = line.split("\t")[1].split("|")[3]
        else:
            newLine[3] = "N/A"

        return "\t".join(newLine) + "\t" + databaseSource + "\t" + " / ".join(taxonomy) + "\n"

