#ifndef XORNODE_H
#define XORNODE_H

#include <AbstractNode.h>


class XORNode : public AbstractNode
{
    public:
        XORNode();
        virtual ~XORNode();
        XORNode(const XORNode& other);
        XORNode& operator=(const XORNode& other);

    private:
        void Process() override;
};

#endif // XORNODE_H
