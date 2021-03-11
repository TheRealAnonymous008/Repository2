#ifndef ADDERNODE_H
#define ADDERNODE_H

#include <AbstractNode.h>


class ADDERNode : public AbstractNode
{
    public:
        ADDERNode();
        virtual ~ADDERNode();
        ADDERNode(const ADDERNode& other);
        ADDERNode& operator=(const ADDERNode& other);

    private:
        void Process() override;
};

#endif // ADDERNODE_H
